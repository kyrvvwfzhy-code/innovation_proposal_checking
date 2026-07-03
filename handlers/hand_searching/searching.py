from sentence_transformers import SentenceTransformer
from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.metrics.pairwise import cosine_similarity

class Searching_Thread(QThread):
    searching_finished = pyqtSignal(list)
    searching_error = pyqtSignal(str)

    def __init__(self, parent, db_embeddings):
        super().__init__()
        self.parent = parent
        self.db_embeddings = db_embeddings
    
    def run(self):
        model_en = SentenceTransformer('all-MiniLM-L6-v2')
        text = self.parent.gui.lineEdit.text()
        try:
            if len(text) == 0:
                pass
            
            elif len(text) > 0:
                embeddings = model_en.encode(text)
                embedding_result = embeddings.tolist()
                names = [item[0] for item in self.db_embeddings]
                embeddings = [item[1] for item in self.db_embeddings]

                similarities = cosine_similarity([embedding_result], embeddings)[0]
                
                max_similarity = float(max(similarities))
                max_index = int(similarities.argmax())
                best_name = names[max_index]
                
                result = [max_similarity, best_name, text]
                self.searching_finished.emit(result)
        except Exception as e:
            self.searching_error.emit(f"Error - {e}")
        