from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.metrics.pairwise import cosine_similarity
from log.logging import logger
import ollama
import numpy as np

class Searching_Thread(QThread):
    searching_finished = pyqtSignal(list)
    searching_error = pyqtSignal(str)

    def __init__(self, parent, db_embeddings_name, db_embeddings_description, db_embeddings_general):
        super().__init__()
        self.parent = parent
        self.db_embeddings_name = db_embeddings_name
        self.db_embeddings_description = db_embeddings_description
        self.db_embeddings_general = db_embeddings_general
        self.model_name = "qwen3-embed"

    def run(self):
        logger.info(f"Использую модель эмбеддингов: {self.model_name}")
        
        text_name = self.parent.gui.plainTextEdit.toPlainText()
        text_description = self.parent.gui.plainTextEdit_2.toPlainText()

        try:
            if len(text_name) == 0 and len(text_description) == 0:
                logger.info(f"SEARCHING - Поля для поиска ПУСТЫЕ!")
                pass

            elif len(text_name) > 0 and len(text_description) == 0:
                logger.info(f"SEARCHING - Поиск по НАИМЕНОВАНИЮ!")
                self.search("name", text_name, self.db_embeddings_name)

            elif len(text_description) > 0 and len(text_name) == 0:
                logger.info(f"SEARCHING - Поиск по ОПИСАНИЮ!")
                self.search("description", text_description, self.db_embeddings_description)

            elif len(text_name) > 0 and len(text_description) > 0:
                logger.info(f"SEARCHING - Поиск по НАИМЕНОВАНИЮ и ОПИСАНИЮ!")
                text = [text_name, text_description]
                self.search("general", text, self.db_embeddings_general)

        except Exception as e:
            self.searching_error.emit(logger.error(f"SEARCHING - {e}"))

    def search(self, value, text, db_embedding):
        if value == "name":
            self.search_process(value, text, db_embedding)
        if value == "description":
            self.search_process(value, text, db_embedding)
        if value == "general":
            self.search_process(value, text, db_embedding)

    def search_process(self, value, text, db_embedding):
        def get_embedding(text):
            if not text:
                return None
            response = ollama.embeddings(
                model=self.model_name,
                prompt=text
            )
            return response["embedding"]

        if value == "name" or value == "description":
            embedding_result = get_embedding(text)
            if embedding_result is None:
                return
            
            names = [item[0] for item in db_embedding]
            embeddings = [item[1] for item in db_embedding]
            
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
            
            if value == "name":
                result = [top_5, text]
            else:
                result = [top_5, "ПОИСК ПО ОПИСАНИЮ"]
            self.searching_finished.emit(result)

        elif value == "general":
            sentences_name = text[0]
            sentences_description = text[1]
            
            embeddings_name = get_embedding(sentences_name)
            embeddings_description = get_embedding(sentences_description)
            
            if embeddings_name is None or embeddings_description is None:
                return
            
            embeddings_result = [embeddings_name, embeddings_description]
            general = self.calculating_general(embeddings_result)

            names = [item[0] for item in db_embedding]
            embedding_general = [item[1] for item in db_embedding]
            similarities_general = cosine_similarity([general], embedding_general)[0]
            
            top_k = min(5, len(similarities_general))
            top_indices = np.argsort(similarities_general)[-top_k:][::-1]
                        
            top_5 = []
            for idx in top_indices:
                top_5.append({
                    'name': names[idx],
                    'similarity': float(similarities_general[idx])
                })
                        
            logger.info(f"Найдено {len(top_5)} похожих документов:")
            for i, item in enumerate(top_5, 1):
                logger.info(f"  {i}. {item['name']} - {item['similarity']:.4f} ({item['similarity']*100:.2f}%)")

            result = [top_5, "ПОИСК ПО НАИМЕНОВАНИЮ И ОПИСАНИЮ"]
            self.searching_finished.emit(result)
            
    def calculating_general(self, embeddings_result):
        name_emb = np.array(embeddings_result[0])
        desc_emb = np.array(embeddings_result[1])
        
        name_emb = name_emb / np.linalg.norm(name_emb)
        desc_emb = desc_emb / np.linalg.norm(desc_emb)
        
        general_emb = (name_emb + desc_emb) / 2
        general_emb = general_emb / np.linalg.norm(general_emb)

        return general_emb