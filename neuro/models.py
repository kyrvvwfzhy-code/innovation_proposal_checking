import torch
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama
from log.logging import logger

def image_encoder():
    try:
        model_path = r"C:\IPC_models\qwen_image_encoder"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Модель загружена через - {device}")
        model = SentenceTransformer(
            model_path,
            device=device
        )
        model.eval()
        return model
    except Exception as e:
            f"Ошибка загрузки модели Qwen3-VL_encoder: {e}"
            raise RuntimeError(f"Ошибка загрузки модели Qwen3-VL_encoder: {e}") from e

def text_embedding():
    try:
        text_embed_model = Llama(
        model_path = r"C:\IPC_models\qwen_text_encoder\Qwen3-Embedding-8B-Q4_K_M.gguf",
        embedding = True,
        n_gpu_layers = 0,
        n_ctx = 8192,
        verbose = False)
        return text_embed_model
    except Exception as e:
        f"Ошибка загрузки модели Qwen3_Embedding: {e}"
        raise RuntimeError(f"Ошибка загрузки модели Qwen3-VL_encoder: {e}") from e

def instruct():
    try:
        instruct_model = Llama(
        model_path = r"C:\IPC_models\qwen_instract\qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf",
        n_gpu_layers = 0,
        n_ctx = 8192,
        chat_format = "qwen",
        verbose=False)
        return instruct_model
    except Exception as e:
        f"Ошибка загрузки модели Qwen2.5-7b-Instruct: {e}"
        raise RuntimeError(f"Ошибка загрузки модели Qwen3-VL_encoder: {e}") from e