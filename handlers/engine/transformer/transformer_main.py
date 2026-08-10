from handlers.engine.transformer.vectorization import Vectorization_Thread
from handlers.engine.transformer.semantic_deduplication import Semantic_deduplication_Thread
from handlers.engine.transformer.searching import Searching_Thread
from handlers.engine.transformer.LLM import LLM_analys_Thread
from data.messagebox import critical_message, question_message
import numpy as np

from data.data import make_response_text, general_text

from log.logging import logger

class Transformer:
    def __init__(self, parent, db, level):
        self.parent = parent
        self.db = db
        self.level = level
        self.thread = None

    def start(self):
        self.vectorization_thread()
    
    def vectorization_thread(self):
        if self.level == "download":
            filename = self.parent.gui.label_4.text()
            self.data = self.db.get_innovation_proposal_info(filename = filename)
            if self.data != None:
                self.thread = Vectorization_Thread(parent = self.parent, name = self.data[0], description = self.data[1])
                self.parent.gui.pushButton_2.setEnabled(False)
                self.parent.gui.pushButton_2.setText("ВЕКТОРИЗАЦИЯ...")
                self.thread.vectorization_finished.connect(self.vectorization_finished)
                self.thread.vectorization_error.connect(self.vectorization_error)
                self.thread.start()
            else:
                pass
        elif self.level == "search":
            logger.info("START - hand_searching")
    
            db_embeddings_name = self.db.get_innovation_proposal_embeddings("name")
            db_embeddings_description = self.db.get_innovation_proposal_embeddings("description")
            db_embeddings_general = self.db.get_innovation_proposal_embeddings("general")
    
    
            if db_embeddings_name != None and db_embeddings_description != None:
                self.thread = Searching_Thread(self.parent, db_embeddings_name, db_embeddings_description, db_embeddings_general)
                self.parent.gui.pushButton_2.setEnabled(False)
                self.thread.searching_finished.connect(self.searching_finished)
                self.thread.searching_error.connect(self.searching_error)
                self.thread.start()
            else:
                logger.debug(f"EMBEDDINGS TABLE - {len(db_embeddings_name)} records")
        
    def vectorization_finished(self, new_embedding):
        self.thread.deleteLater()
        name = new_embedding[0]
        description = new_embedding[1]
        general = self.calculating_general(name, description)

        db_embeddings = self.db.get_innovation_proposal_embeddings("general")
        if db_embeddings:
            self.semantic_deduplication_thread(general, db_embeddings)
        if db_embeddings == None:
            critical_message(self.parent, "Журнал пустой")
            self.parent.gui.pushButton_2.setEnabled(True)
            self.parent.gui.pushButton_2.setText("Начать поиск")
        self.filename = self.parent.gui.label_4.text()
        self.db.add_innovation_proposal_embeddings(self.filename, name, description, general)

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
        response_text = make_response_text(result, self.data[0])
        general = general_text(response_text, "Формируется...")
        self.parent.gui.plainTextEdit_2.setPlainText(general)
        self.LLM_analys(result)

    def semantic_deduplication_error(self, error):
        print(f"errorsem - {error}")
        self.thread.deleteLater()

    def searching_finished(self, result):
            self.thread.deleteLater()
            logger.info("SEARECHING is Ready")
            response_text = make_response_text(result[0], result[1])
            general = general_text(response_text, "Формируется...")
            self.parent.gui.plainTextEdit_3.setPlainText(general)
            self.LLM_analys(result)
        
    def searching_error(self, error):
        logger.error(f"SEARCHING - {error}")
        self.thread.deleteLater()

    def LLM_analys(self, result):
        if self.level == "download":
            self.parent.gui.pushButton_2.setText("АНАЛИЗ ЯЗЫКОВОЙ МОДЕЛИ...")
            self.thread = LLM_analys_Thread(result, self.data[0])
            self.thread.LLM_analys_finished.connect(self.LLM_analys_finished)
            self.thread.LLM_analys_error.connect(self.LLM_analys_error)
            self.thread.start()
        elif self.level == "search":
            self.thread = LLM_analys_Thread(result[0], result[1])
            self.thread.LLM_analys_finished.connect(self.LLM_analys_finished)
            self.thread.LLM_analys_error.connect(self.LLM_analys_error)
            self.thread.start()

    def LLM_analys_finished(self, result):
        if self.level == "download":
            general = general_text(result[0], result[1])
            self.parent.gui.plainTextEdit_2.setPlainText(general)
            reply = question_message(self.parent, "Добавить в базу", result[2])
            if reply == False:
                self.db.delete_innovation_proposal(self.filename[:-4])
            self.parent.gui.pushButton_2.setEnabled(True)
            self.parent.gui.pushButton_2.setText("Начать поиск")
            self.thread.deleteLater()
        elif self.level == "search":
            general = general_text(result[0], result[1])
            self.parent.gui.plainTextEdit_3.setPlainText(general)
            self.parent.gui.pushButton_2.setEnabled(True)
            logger.info("LLM_analys is Ready")
            self.thread.deleteLater()
    
    def LLM_analys_error(self, error):
        if self.level == "download":
            print(f"errorllm - {error}")
            self.thread.deleteLater()
        elif self.level == "search":
            logger.error(f"LLM_analys - {error}")
            self.thread.deleteLater()

