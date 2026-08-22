from PyQt5.QtCore import QThread, pyqtSignal

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

class Semantic_deduplication_Thread(QThread):
    semantic_deduplication_finished = pyqtSignal(list)
    semantic_deduplication_error = pyqtSignal(str)

    def __init__(self, general, db_embeddings):
        super().__init__()
        self.general = general
        self.db_embeddings = db_embeddings
        
    def run(self):
        try:
            names = [item[0] for item in self.db_embeddings]
            embedding_general = [item[1] for item in self.db_embeddings]
            similarities_general = cosine_similarity([self.general], embedding_general)[0]

            top_k = min(5, len(similarities_general))
            top_indices = np.argsort(similarities_general)[-top_k:][::-1]  
            
            result = []
            for idx in top_indices:
                result.append({
                    'name': names[idx],
                    'similarity': float(similarities_general[idx])
                })
                
            self.semantic_deduplication_finished.emit(result)
        except Exception as e:
            self.semantic_deduplication_error.emit(f"Error - {e}")