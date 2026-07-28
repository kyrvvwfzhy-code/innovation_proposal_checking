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
        self.model_path = r"/home/niyazabiy/models--sentence-transformers--all-MiniLM-L6-v2"
        logger.info(f"ПУТЬ МОДЕЛИ - {self.model_path}")
        self.model_en = SentenceTransformer(self.model_path)

        text_name = self.parent.gui.plainTextEdit.toPlainText()
        text_description = self.parent.gui.plainTextEdit_2.toPlainText()

        try:
            if len(text_name) == 0 and len(text_description) == 0:
                logger.info(f"SEARCHING - Поля пустые!")
                pass

            # ПОИСК ПО НАИМЕНОВАНИЮ

            elif len(text_name) > 0 and len(text_description) == 0:
                logger.info(f"SEARCHING - Поиск по НАИМЕНОВАНИЮ!")
                self.main_func_name(text_name)

            # ПОИСК ПО ОПИСАНИЮ

            elif len(text_description) > 0 and len(text_name) < 0 :
                logger.info(f"SEARCHING - Поиск по ОПИСАНИЮ!")
                self.main_func_name(text_description)

            # ПОИСК ПО НАИМЕНВОАНИЮ И ОПИСАНИЮ

            elif len(text_name) > 0 and len(text_description) > 0:
                logger.info(f"SEARCHING - Поиск по НАИМЕНОВАНИЮ и ОПИСАНИЮ!")
        except Exception as e:
            self.searching_error.emit(logger.error(f"SEARCHING - {e}"))

    def main_func_name(self, values):
        embeddings = self.model_en.encode(values)
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
            
        logger.debug(f"LINEEDIT - {len(values)}")
        logger.info(f"SEARCHING - {top_5}")
        logger.info(f"Найдено {len(top_5)} похожих документов:")
        for i, item in enumerate(top_5, 1):
            logger.info(f"  {i}. {item['name']} - {item['similarity']:.4f} ({item['similarity']*100:.2f}%)")
        
        
        result = [top_5, values]
        self.searching_finished.emit(result)


    def main_func_description(self, values):
        embeddings = self.model_en.encode(values)
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
            
        logger.debug(f"LINEEDIT - {len(values)}")
        logger.info(f"SEARCHING - {top_5}")
        logger.info(f"Найдено {len(top_5)} похожих документов:")
        for i, item in enumerate(top_5, 1):
            logger.info(f"  {i}. {item['name']} - {item['similarity']:.4f} ({item['similarity']*100:.2f}%)")
        
        
        result = [top_5, values]
        self.searching_finished.emit(result)

        