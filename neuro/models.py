import torch
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

def image_encoder():
    try:
        model_path = r"C:\models\qwen_image_encoder"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        model = SentenceTransformer(
            model_path,
            device=device
        )
        model.eval()
        
        return model
    except Exception as e:
            f"Ошибка загрузки модели Qwen_image_encoder: {str(e)}"

def text_embedding():
    try:
        text_embed_model = Llama(
        model_path = r"C:\models\qwen_text_embed\Qwen3-Embedding-8B-Q4_K_M.gguf",
        embedding = True,
        n_gpu_layers = 0,
        n_ctx = 8192,
        verbose = False)

        return text_embed_model
    except Exception as e:
        f"Ошибка загрузки модели Qwen3_Embedding: {str(e)}"

def instruct():
    try:
        instruct_model = Llama(
        model_path = r"C:\models\qwen_instract\qwen2.5-coder-7b-instruct-q4_k_m.gguf",
        n_gpu_layers = 0,
        n_ctx = 8192,
        chat_format = "qwen",
        verbose=False)

        return instruct_model
    except Exception as e:
        f"Ошибка загрузки модели Qwen2.5_Instruct: {str(e)}"