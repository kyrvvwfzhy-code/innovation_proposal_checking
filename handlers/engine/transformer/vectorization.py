from sentence_transformers import SentenceTransformer
from PyQt5.QtCore import QThread, pyqtSignal
from log.logging import logger

class Vectorization_Thread(QThread):
    vectorization_finished = pyqtSignal(object)
    vectorization_error = pyqtSignal(str)

    def __init__(self, parent, name, description = None):
        super().__init__()
        self.parent = parent
        self.name = name
        self.description = description
    
    def run(self):
        self.model_path = r"/home/niyazabiy/models--sentence-transformers--all-MiniLM-L6-v2"
        logger.info(f"ПУТЬ МОДЕЛИ - {self.model_path}")
        self.model_en = SentenceTransformer(self.model_path)
        sentences_name = self.name
        sentences_description = self.description
        try:
            if sentences_description is None:
                embeddings_name = self.model_en.encode(sentences_name)
                embedding_name_result = embeddings_name.tolist()
                self.vectorization_finished.emit(embedding_name_result)

            elif len(sentences_name) == 0 and len(sentences_description) == 0:
                pass
            
            elif len(sentences_name) > 0 and len(sentences_description) > 0:
                embeddings_name = self.model_en.encode(sentences_name)
                embedding_name_result = embeddings_name.tolist()

                embeddings_description = self.model_en.encode(sentences_description)
                embedding_description_result = embeddings_description.tolist()

                embeddings_result = [embedding_name_result, embedding_description_result]
                self.vectorization_finished.emit(embeddings_result)
        except Exception as e:
            self.vectorization_error.emit(f"Error - {e}")