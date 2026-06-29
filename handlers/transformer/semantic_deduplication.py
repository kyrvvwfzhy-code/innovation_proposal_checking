from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.metrics.pairwise import cosine_similarity

class Semantic_deduplication_Thread(QThread):
    semantic_deduplication_finished = pyqtSignal(list)
    semantic_deduplication_error = pyqtSignal(str)

    def __init__(self, new_embedding, db_embeddings):
        super().__init__()
        self.new_embedding = new_embedding
        self.db_embeddings = db_embeddings
        
    def run(self):
        try:
            names = [item[0] for item in self.db_embeddings]
            embeddings = [item[1] for item in self.db_embeddings]

            similarities = cosine_similarity([self.new_embedding], embeddings)[0]
            
            max_similarity = float(max(similarities))
            max_index = int(similarities.argmax())
            best_name = names[max_index]
            
            result = [max_similarity, best_name]

            self.semantic_deduplication_finished.emit(result)
        except Exception as e:
            self.semantic_deduplication_error.emit(f"Error - {e}")