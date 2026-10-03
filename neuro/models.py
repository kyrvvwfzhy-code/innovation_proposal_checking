import torch
from sentence_transformers import SentenceTransformer
import os

def image_encoder():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)

        model_path = os.path.join(root_dir, "neuro", "Qwen_image_encoder")

        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        model = SentenceTransformer(
            model_path,
            device=device
        )
        model.eval()
        
        return model

    except Exception as e:
            f"Ошибка загрузки модели: {str(e)}"