from PyQt5.QtCore import QThread, pyqtSignal

from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

class Vectorization_thread(QThread):
    vectorization_finished = pyqtSignal(list)
    vectorization_error = pyqtSignal(str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.load_CLIP_model()

    def run(self):
        try:
            image = Image.open(self.image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt")
            with torch.no_grad():
                output = self.model.get_image_features(**inputs)
                embedding = output.pooler_output
                image_embedding = embedding.detach().cpu().numpy().flatten().tolist()
        
            self.vectorization_finished.emit(image_embedding)
        except Exception as e:
            self.vectorization_error.emit(str(e))

    def load_CLIP_model(self):
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