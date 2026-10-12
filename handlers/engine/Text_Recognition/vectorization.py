from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import os
from PIL import Image
import torch

class Vectorization_Thread(QThread):
    vectorization_data_finished = pyqtSignal(str)
    vectorization_data_error = pyqtSignal(str)

    def __init__(self, db, filename_list, names, descriptions, image_encoder_model, text_embedding_model, tmp_path = None):
        super().__init__()
        self.db = db
        self.filename_list = filename_list
        self.names = names
        self.descriptions = descriptions
        self.image_encoder_model = image_encoder_model
        self.text_embedding_model = text_embedding_model
        self.tmp_path = tmp_path

    def run(self):
        try:
            self.all_image_embeddings = self.get_image_embedding()

            def get_embedding(text):
                if not text:
                    return None
                response = self.text_embedding_model.create_embedding(text)
                return response["data"][0]["embedding"]

            for idx, filename in enumerate(self.filename_list):
                name = self.names[idx]
                description = self.descriptions[idx]
                
                cleaned_name = self.clean_text(name)
                
                embeddings_name = get_embedding(cleaned_name)
                embeddings_description = get_embedding(description)
                
                new_embedding_general = self.calculating_general(embeddings_name, embeddings_description)
                
                embedding_image = self.all_image_embeddings[idx]

                self.db.add_innovation_proposal_embeddings(
                    filename, 
                    embeddings_name, 
                    embeddings_description, 
                    new_embedding_general,
                    embedding_image
                )
    
            self.vectorization_data_finished.emit("Эмбеддинги созданы")
            
        except Exception as e:
            self.vectorization_data_error.emit(f"Error - {e}")

    def calculating_general(self, name, description):
        name_emb = np.array(name)
        desc_emb = np.array(description)
        
        name_emb = name_emb / np.linalg.norm(name_emb)
        desc_emb = desc_emb / np.linalg.norm(desc_emb)
        
        general_emb = (name_emb + desc_emb) / 2
        general_emb = general_emb / np.linalg.norm(general_emb)
        
        return general_emb
    
    def clean_text(self, elements):
        return ' '.join(str(elements).replace('\n', ' ').replace('\x0c', ' ').split()).strip()

    def get_image_embedding(self):
        folder_path = self.tmp_path

        if os.path.exists(folder_path):
            paths = []

            for filename in os.listdir(folder_path):
                if filename.startswith('3'):
                    full_path = os.path.join(folder_path, filename)

                    if os.path.isfile(full_path):
                        paths.append(full_path)

            files = sorted(paths)
            result_list = []

            for path in files:
                image = Image.open(path).convert("RGB")
                new_size = (224, 224)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                with torch.no_grad():
                    embedding = self.image_encoder_model.encode(
                        [image],
                        normalize_embeddings=True,
                        batch_size=1,
                        convert_to_numpy=True
                    )

                image_embedding = embedding[0].flatten().tolist()
                result_list.append(image_embedding)

            return result_list
