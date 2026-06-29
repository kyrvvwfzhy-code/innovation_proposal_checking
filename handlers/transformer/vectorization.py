from sentence_transformers import SentenceTransformer
from PyQt5.QtCore import QThread, pyqtSignal

class Vectorization_Thread(QThread):
    vectorization_finished = pyqtSignal(object)
    vectorization_error = pyqtSignal(str)

    def __init__(self, parent, text):
        super().__init__()
        self.parent = parent
        self.text = text
    
    def run(self):
        model_en = SentenceTransformer('all-MiniLM-L6-v2')
        sentences = self.text
        try:
            if len(sentences) == 0:
                pass
            
            elif len(sentences) > 0:
                embeddings = model_en.encode(sentences)
                embedding_result = embeddings.tolist()
                self.vectorization_finished.emit(embedding_result)
        except Exception as e:
            self.vectorization_error.emit(f"Error - {e}")