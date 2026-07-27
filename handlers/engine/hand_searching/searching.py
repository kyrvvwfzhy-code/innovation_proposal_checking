from sentence_transformers import SentenceTransformer
from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.metrics.pairwise import cosine_similarity
from log.logging import logger
import os
import numpy as np

class Searching_Thread(QThread):
    searching_finished = pyqtSignal(list)
    searching_error = pyqtSignal(str)

    def __init__(self, parent, db_embeddings):
        super().__init__()
        self.parent = parent
        self.db_embeddings = db_embeddings
    
    def run(self):
        model_path = r"/home/niyazabiy/models--sentence-transformers--all-MiniLM-L6-v2"
        logger.info(f"ПУТЬ МОДЕЛИ - {model_path}")
        model_en = SentenceTransformer(model_path)
        text = self.parent.gui.plainTextEdit.toPlainText()
        try:
            if len(text) == 0:
                pass
            
            elif len(text) > 0:
                embeddings = model_en.encode(text)
                embedding_result = embeddings.tolist()
                names = [item[0] for item in self.db_embeddings]
                embeddings = [item[1] for item in self.db_embeddings]

                similarities = cosine_similarity([embedding_result], embeddings)[0]
                
                top_k = min(5, len(similarities))
                top_indices = np.argsort(similarities)[-top_k:][::-1]  
        
                top_5 = []
                for idx in top_indices:
                    top_5.append({
                        'name': names[idx],
                        'similarity': float(similarities[idx])
                    })
                logger.debug(f"LINEEDIT - {len(text)}")
                logger.info(f"SEARCHING - {top_5}")
                logger.info(f"Найдено {len(top_5)} похожих документов:")
                for i, item in enumerate(top_5, 1):
                    logger.info(f"  {i}. {item['name']} - {item['similarity']:.4f} ({item['similarity']*100:.2f}%)")


                result = [top_5, text]
                self.searching_finished.emit(result)

        except Exception as e:
            self.searching_error.emit(logger.error(f"SEARCHING - {e}"))
        