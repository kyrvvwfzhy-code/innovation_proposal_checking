from PyQt5.QtCore import QThread, pyqtSignal

from PIL import Image
import torch

class Vectorization_thread(QThread):
    vectorization_finished = pyqtSignal(list)
    vectorization_error = pyqtSignal(str)

    def __init__(self, image_path, model):
        super().__init__()
        self.image_path = image_path
        self.model = model

    def run(self):
        try:
            image = Image.open(self.image_path).convert("RGB")
            new_size = (224, 224)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            with torch.no_grad():
                embedding = self.model.encode(
                [image],
                normalize_embeddings=True,
                batch_size=1,
                convert_to_numpy=True
                )
                image_embedding = embedding[0].flatten().tolist()
            self.vectorization_finished.emit(image_embedding)
        except Exception as e:
            self.vectorization_error.emit(str(e))