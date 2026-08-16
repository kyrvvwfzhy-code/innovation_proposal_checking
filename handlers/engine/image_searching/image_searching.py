from PyQt5.QtCore import QThread, pyqtSignal

from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

class Image_searching_thread(QThread):
    image_searching_finished = pyqtSignal(list)
    image_searching_error = pyqtSignal(str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.load_model()

    def run(self):
        try:
            image = Image.open(self.image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt")
            with torch.no_grad():
                output = self.model.get_image_features(**inputs)
                embedding = output.pooler_output
                result = embedding.detach().cpu().numpy().flatten().tolist()
            self.image_searching_finished.emit(result)

        except Exception as e:
            self.image_searching_error.emit(f"Error - {e}")

    def load_model(self):
        model_path = r"C:\CLIP"
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
