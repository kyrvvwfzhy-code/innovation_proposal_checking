from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QThread, pyqtSignal, QUrl

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

class Semantic_deduplication_Thread(QThread):
    semantic_deduplication_finished = pyqtSignal(list)
    semantic_deduplication_error = pyqtSignal(str)

    def __init__(self, general, db_embeddings, db):
        super().__init__()
        self.general = general
        self.db_embeddings = db_embeddings
        self.db = db
        
    def run(self):
        try:
            names = [item[0] for item in self.db_embeddings]
            embedding_general = [item[1] for item in self.db_embeddings]
            similarities_general = cosine_similarity([self.general], embedding_general)[0]

            top_k = min(5, len(similarities_general))
            top_indices = np.argsort(similarities_general)[-top_k:][::-1]
            
            result = []
            for idx in top_indices:
                name = names[idx]
                file_path = self.db.get_filepath_from_innovation_proposal_by_name(name)
                url = QUrl.fromLocalFile(str(file_path)).toString() if file_path else ""
                result.append({
                    'name': name,
                    'similarity': float(similarities_general[idx]),
                    'url': url
                })
                
            self.semantic_deduplication_finished.emit(result)
        except Exception as e:
            self.semantic_deduplication_error.emit(f"Error - {e}")