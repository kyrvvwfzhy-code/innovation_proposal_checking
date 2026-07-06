from PyQt5.QtCore import QThread, pyqtSignal
from sentence_transformers import SentenceTransformer
import os

class Embedding_data_Thread(QThread):
    embedding_data_finished = pyqtSignal(str)
    embedding_data_error = pyqtSignal(str)

    def __init__(self, db, filename_list, names):
        super().__init__()
        self.db = db
        self.filename_list = filename_list
        self.names = names

    def run(self):
        try:
            model_en = SentenceTransformer('all-MiniLM-L6-v2')
            
            for idx, filename in enumerate(self.filename_list):
                name = self.names[idx]
                
                cleaned_name = self.clean_text(name)
                
                embeddings = model_en.encode(cleaned_name)
                new_embedding = embeddings.tolist()
                
                self.db.add_embedding(filename, new_embedding)
                text = f"✅ Эмбеддинг для: {os.path.basename(filename)} → {cleaned_name[:50]}..."

            self.embedding_data_finished.emit(text)
            
        except Exception as e:
            self.embedding_data_error.emit(f"Error - {e}")
    
    def clean_text(self, elements):
        return ' '.join(str(elements).replace('\n', ' ').replace('\x0c', ' ').split()).strip()