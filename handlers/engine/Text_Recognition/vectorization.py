from PyQt5.QtCore import QThread, pyqtSignal
import ollama
import numpy as np
import os
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

class Vectorization_Thread(QThread):
    vectorization_data_finished = pyqtSignal(str)
    vectorization_data_error = pyqtSignal(str)

    def __init__(self, db, filename_list, names, descriptions):
        super().__init__()
        self.db = db
        self.filename_list = filename_list
        self.names = names
        self.descriptions = descriptions
        self.model_name = "qwen3-embed"
        self.load_image_model()
        self.all_image_embeddings = self.get_image_embedding()

    def run(self):
        try: 
            def get_embedding(text):
                if not text:
                    return None
                response = ollama.embeddings(
                    model=self.model_name,
                    prompt=text
                )
                return response["embedding"]

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
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            paths = []
            for filename in os.listdir(folder_path):
                if filename.startswith('3'):
                    full_path = os.path.join(folder_path, filename)
                    if os.path.isfile(full_path):
                        paths.append(full_path)
            file = sorted(paths)

            result_list = []

            for paths in file:
                if os.path.basename(paths).startswith('3'): 
                    image = Image.open(paths).convert("RGB")
                    inputs = self.processor(images=image, return_tensors="pt")
                    with torch.no_grad():
                        output = self.model.get_image_features(**inputs)
                        embedding = output.pooler_output
                        result = embedding.detach().cpu().numpy().flatten().tolist()
                    result_list.append(result)

            return result_list
    
    def load_image_model(self):
        model_path = r"/home/niyazabiy/Рабочий стол/AI models/ENCODER/CLIP"
        self.processor = CLIPProcessor.from_pretrained(
                    model_path,
                    local_files_only=True
                )

        self.model = CLIPModel.from_pretrained(
                    model_path,
                    local_files_only=True
                )

        self.model.eval()

        self.device = torch.device(
                    "cuda" if torch.cuda.is_available() else "cpu"
                )

        self.model.to(self.device)

        print("✅ Модель CLIP загружена успешно!")
        print(f"✅ Устройство: {self.device}")
