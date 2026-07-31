from PyQt5.QtCore import QThread, pyqtSignal
from sentence_transformers import SentenceTransformer
import os
import numpy as np

class Embedding_data_Thread(QThread):
    embedding_data_finished = pyqtSignal(str)
    embedding_data_error = pyqtSignal(str)

    def __init__(self, db, filename_list, names, descriptions):
        super().__init__()
        self.db = db
        self.filename_list = filename_list
        self.names = names
        self.descriptions = descriptions

    def run(self):
        try:
            model_en = SentenceTransformer('all-MiniLM-L6-v2')
            
            for idx, filename in enumerate(self.filename_list):
                name = self.names[idx]
                description = self.descriptions[idx]
                
                cleaned_name = self.clean_text(name)
                
                embeddings_name = model_en.encode(cleaned_name)
                embeddings_description = model_en.encode(description)

                new_embedding_name = embeddings_name.tolist()
                new_embedding_description = embeddings_description.tolist()
                new_embedding_general = self.calculating_general(embeddings_name, embeddings_description)
                
                self.db.add_innovation_proposal_embeddings(filename, new_embedding_name, new_embedding_description, new_embedding_general)
    
            self.embedding_data_finished.emit("Эмбеддинги созданы")
            
        except Exception as e:
            self.embedding_data_error.emit(f"Error - {e}")

    def calculating_general(self, name, description):
            name_emb = np.array(name)
            desc_emb = np.array(description)
            
            name_emb = name_emb / np.linalg.norm(name_emb)
            desc_emb = desc_emb / np.linalg.norm(desc_emb)
            
            general_emb = (name_emb + desc_emb) / 2
            general_emb = general_emb / np.linalg.norm(general_emb)
    
            return general_emb
    
    def clean_text(self, elements):
        return ' '.join(str(elements).replace('\n', ' ').replace('\x0c', ' ').split()).strip()