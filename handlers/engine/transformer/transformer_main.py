from handlers.engine.transformer.vectorization import Vectorization_Thread
from handlers.engine.transformer.semantic_deduplication import Semantic_deduplication_Thread
from handlers.engine.transformer.LLM import LLM_analys_Thread
from data.messagebox import critical_message, question_message
import numpy as np


class Vectorization:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None

    def start(self):
        self.vectorization_thread()
    
    def vectorization_thread(self):
        filename = self.parent.gui.label_4.text()
        self.data = self.db.get_name_description(filename)
        if self.data != None:
            self.thread = Vectorization_Thread(self.parent, self.data[0], self.data[1])
            self.parent.gui.pushButton_2.setEnabled(False)
            self.parent.gui.pushButton_2.setText("ВЕКТОРИЗАЦИЯ...")
            self.thread.vectorization_finished.connect(self.vectorization_finished)
            self.thread.vectorization_error.connect(self.vectorization_error)
            self.thread.start()
        else:
            pass
    
    def vectorization_finished(self, new_embedding):
        self.thread.deleteLater()
        
        name = new_embedding[0]
        description = new_embedding[1]

        general = self.calculating_general(name, description)

        db_embeddings = self.db.get_embeddings()
        if db_embeddings:
            self.semantic_deduplication_thread(general, db_embeddings)
        if db_embeddings == None:
            critical_message(self.parent, "Журнал пустой")
            self.parent.gui.pushButton_2.setEnabled(True)
            self.parent.gui.pushButton_2.setText("Начать поиск")
        self.filename = self.parent.gui.label_4.text()
        self.db.add_embedding(self.filename, name, description, general)

    def calculating_general(self, name, description):
        name_emb = np.array(name)
        desc_emb = np.array(description)
        
        name_emb = name_emb / np.linalg.norm(name_emb)
        desc_emb = desc_emb / np.linalg.norm(desc_emb)
        
        general_emb = (name_emb + desc_emb) / 2
        general_emb = general_emb / np.linalg.norm(general_emb)

        return general_emb

    def vectorization_error(self, error):
        print(f"erroremb - {error}")
        self.thread.deleteLater()

    def semantic_deduplication_thread(self, general, db_embeddings):
        self.parent.gui.pushButton_2.setText("СЕМАНТИЧЕСКИЙ ПОИСК...")
        self.thread = Semantic_deduplication_Thread(general, db_embeddings)
        self.thread.semantic_deduplication_finished.connect(self.semantic_deduplication_finished)
        self.thread.semantic_deduplication_error.connect(self.semantic_deduplication_error)
        self.thread.start()
    
    def semantic_deduplication_finished(self, result):
        self.thread.deleteLater()
        self.LLM_analys(result)

    def semantic_deduplication_error(self, error):
        print(f"errorsem - {error}")
        self.thread.deleteLater()

    def LLM_analys(self, result):
        self.parent.gui.pushButton_2.setText("АНАЛИЗ ЯЗЫКОВОЙ МОДЕЛИ...")
        self.thread = LLM_analys_Thread(result, self.data[0])
        self.thread.LLM_analys_finished.connect(self.LLM_analys_finished)
        self.thread.LLM_analys_error.connect(self.LLM_analys_error)
        self.thread.start()

    def LLM_analys_finished(self, result):
        self.parent.gui.plainTextEdit_2.setPlainText(result[0])
        reply = question_message(self.parent, "Добавить в базу", result[1])
        if reply == False:
            self.db.delete_embeddings(self.filename)
        self.parent.gui.pushButton_2.setEnabled(True)
        self.parent.gui.pushButton_2.setText("Начать поиск")
        self.thread.deleteLater()
    
    def LLM_analys_error(self, error):
        print(f"errorllm - {error}")
        self.thread.deleteLater()

