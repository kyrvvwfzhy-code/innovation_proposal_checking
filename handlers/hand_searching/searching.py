from sentence_transformers import SentenceTransformer
from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.metrics.pairwise import cosine_similarity
from log.logging import logger
import os

class Searching_Thread(QThread):
    searching_finished = pyqtSignal(list)
    searching_error = pyqtSignal(str)

    def __init__(self, parent, db_embeddings):
        super().__init__()
        self.parent = parent
        self.db_embeddings = db_embeddings
    
    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
            
        model_path = os.path.join(
                project_root, 
                'data', 
                'models--sentence-transformers--all-MiniLM-L6-v2'
            )
        
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
                
                max_similarity = float(max(similarities))
                max_index = int(similarities.argmax())
                best_name = names[max_index]
                
                result = [max_similarity, best_name, text]
                self.searching_finished.emit(result)
            logger.debug(f"LINEEDIT - {len(text)}")
            logger.info(f"SEARCHING - {result}")
        except Exception as e:
            self.searching_error.emit(logger.error(f"SEARCHING - {e}"))
        