from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from log.logging import logger

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
            
            logger.info(f"Найдено {len(result)} похожих документов:")
            for i, item in enumerate(result, 1):
                logger.info(f"  {i}. {item['name']} - {item['similarity']:.4f} ({item['similarity']*100:.2f}%)")

            self.semantic_deduplication_finished.emit(result)
        except Exception as e:
            self.semantic_deduplication_error.emit(f"Error - {e}")