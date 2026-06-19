from sentence_transformers import SentenceTransformer
from PyQt5.QtCore import QThread, pyqtSignal

class Embedding_Thread(QThread):
    embedding_finished = pyqtSignal(object)
    embedding_error = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    
    def run(self):
        model_en = SentenceTransformer('all-MiniLM-L6-v2')
        sentences = self.parent.gui.plainTextEdit.toPlainText()
        try:
            if len(sentences) == 0:
                pass
            
            elif len(sentences) > 0:
                embeddings = model_en.encode(sentences)
                embedding_result = [embeddings.tolist()]
                self.embedding_finished.emit(embedding_result)
        except Exception as e:
            self.embedding_error.emit(f"Error - {e}")