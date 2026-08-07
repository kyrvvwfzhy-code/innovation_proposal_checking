import ollama
from PyQt5.QtCore import QThread, pyqtSignal
from log.logging import logger

class Vectorization_Thread(QThread):
    vectorization_finished = pyqtSignal(object)
    vectorization_error = pyqtSignal(str)

    def __init__(self, parent, name, level = None, description=None):
        super().__init__()
        self.parent = parent
        self.name = name
        self.level = level
        self.description = description
        self.model_name = "qwen3-embed"  

    def run(self):
        logger.info(f"Использую модель эмбеддингов: {self.model_name}")
        
        sentences_name = self.name
        sentences_description = self.description

        if self.level == "vector_update":
            try:
                def get_embedding(text):
                    if not text:
                        return None
                    response = ollama.embeddings(
                        model=self.model_name,
                        prompt=text 
                    )
                    return response["embedding"] 
                if sentences_name != None:
                    new_embeddings = []
                    for names in sentences_name:
                        embedding = get_embedding(names)
                        new_embeddings.append(embedding)
                        
                    self.vectorization_finished.emit(new_embeddings)
                
            except Exception as e:
                logger.error(f"Ошибка векторизации: {e}")
                self.vectorization_error.emit(f"Error - {e}")      
        else:
            try:
                def get_embedding(text):
                    if not text:
                        return None
                    response = ollama.embeddings(
                        model=self.model_name,
                        prompt=text 
                    )
                    return response["embedding"] 

                if sentences_description is None:
                    embeddings_name = get_embedding(sentences_name)
                    if embeddings_name is not None:
                        self.vectorization_finished.emit(embeddings_name)

                elif len(sentences_name) == 0 and len(sentences_description) == 0:
                    pass
                
                elif len(sentences_name) > 0 and len(sentences_description) > 0:
                    embeddings_name = get_embedding(sentences_name)
                    embeddings_description = get_embedding(sentences_description)
                    
                    if embeddings_name is not None and embeddings_description is not None:
                        embeddings_result = [embeddings_name, embeddings_description]
                        self.vectorization_finished.emit(embeddings_result)
                        
            except Exception as e:
                logger.error(f"Ошибка векторизации: {e}")
                self.vectorization_error.emit(f"Error - {e}")