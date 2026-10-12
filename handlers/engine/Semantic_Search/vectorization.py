from PyQt5.QtCore import QThread, pyqtSignal
from PIL import Image
import torch
import os

class Vectorization_Thread(QThread):
    vectorization_finished = pyqtSignal(object)
    vectorization_error = pyqtSignal(str)

    def __init__(self, parent, name, level = None, description = None, image_encoder_model = None, text_embedding_model = None, tmp_path = None):
        super().__init__()
        self.parent = parent
        self.name = name
        self.level = level
        self.description = description
        self.image_encoder_model = image_encoder_model
        self.text_embedding_model = text_embedding_model
        self.tmp_path = tmp_path

    def run(self):   
        sentences_name = self.name
        sentences_description = self.description

        if self.level == "vector_update":
            try:
                def get_embedding(text):
                    if not text:
                        return None
                    response = self.text_embedding_model.create_embedding(text)
                    return response["data"][0]["embedding"] 
                if sentences_name != None:
                    new_embeddings = []
                    for names in sentences_name:
                        embedding = get_embedding(names)
                        new_embeddings.append(embedding)
                        
                    self.vectorization_finished.emit(new_embeddings)
                
            except Exception as e:
                self.vectorization_error.emit(f"Error - {e}")      
        else:
            try:
                def get_embedding(text):
                    if not text:
                        return None
                    response = self.text_embedding_model.create_embedding(text)
                    return response["data"][0]["embedding"]

                if sentences_description is None:
                    embeddings_name = get_embedding(sentences_name)
                    if embeddings_name is not None:
                        self.vectorization_finished.emit(embeddings_name)

                elif len(sentences_name) == 0 and len(sentences_description) == 0:
                    pass
                
                elif len(sentences_name) > 0 and len(sentences_description) > 0:
                    embeddings_name = get_embedding(sentences_name)
                    embeddings_description = get_embedding(sentences_description)
                    embedding_image = self.get_image_embedding()
                    
                    if embeddings_name is not None and embeddings_description is not None:
                        embeddings_result = [embeddings_name, embeddings_description, embedding_image]
                        self.vectorization_finished.emit(embeddings_result)
                        
            except Exception as e:
                self.vectorization_error.emit(f"Error - {e}")

    def get_image_embedding(self):
        image_path = None
        folder_path = self.tmp_path
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.startswith('3'):
                    full_path = os.path.join(folder_path, filename)
                    if os.path.isfile(full_path):
                        image_path = full_path
                        break

        image = Image.open(image_path).convert("RGB")
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
            result = image_embedding
        return result