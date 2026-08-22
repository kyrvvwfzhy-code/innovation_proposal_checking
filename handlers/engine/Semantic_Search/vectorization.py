from PyQt5.QtCore import QThread, pyqtSignal
import ollama
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import os

class Vectorization_Thread(QThread):
    vectorization_finished = pyqtSignal(object)
    vectorization_error = pyqtSignal(str)

    def __init__(self, parent, name, level = None, description=None):
        super().__init__()
        self.parent = parent
        self.name = name
        self.level = level
        self.description = description
        self.model_name = "qwen3-embed"
        self.load_image_model()

    def run(self):   
        sentences_name = self.name
        sentences_description = self.description

        if self.level == "vector_update":
            try:
                def get_embedding(text):
                    if not text:
                        return None
                    response = ollama.embeddings(
                        model=self.model_name,
                        prompt=text 
                    )
                    return response["embedding"] 
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
                    response = ollama.embeddings(
                        model=self.model_name,
                        prompt=text 
                    )
                    return response["embedding"] 

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
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if filename.startswith('3'):
                    full_path = os.path.join(folder_path, filename)
                    if os.path.isfile(full_path):
                        image_path = full_path
                        break

        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            output = self.model.get_image_features(**inputs)
            embedding = output.pooler_output
            result = embedding.detach().cpu().numpy().flatten().tolist()
        return result
              
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