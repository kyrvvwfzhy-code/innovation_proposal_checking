from sentence_transformers import SentenceTransformer
from PyQt5.QtCore import QThread, pyqtSignal

class Vectorization_Thread(QThread):
    vectorization_finished = pyqtSignal(object)
    vectorization_error = pyqtSignal(str)

    def __init__(self, parent, name, description):
        super().__init__()
        self.parent = parent
        self.name = name
        self.description = description
    
    def run(self):
        model_en = SentenceTransformer('all-MiniLM-L6-v2')
        sentences_name = self.name
        sentences_description = self.description
        try:
            if len(sentences_name) == 0 and len(sentences_description) == 0:
                pass
            
            elif len(sentences_name) > 0 and len(sentences_description) > 0:
                embeddings_name = model_en.encode(sentences_name)
                embedding_name_result = embeddings_name.tolist()

                embeddings_description = model_en.encode(sentences_description)
                embedding_description_result = embeddings_description.tolist()

                embeddings_result = [embedding_name_result, embedding_description_result]
                self.vectorization_finished.emit(embeddings_result)
        except Exception as e:
            self.vectorization_error.emit(f"Error - {e}")