from PyQt5.QtWidgets import QPushButton 
from PyQt5 import QtCore 

from handlers.engine.Semantic_Search.vectorization import Vectorization_Thread
from handlers.engine.Semantic_Search.semantic_deduplication import Semantic_deduplication_Thread
from handlers.engine.Semantic_Search.searching import Searching_Thread
from handlers.engine.Semantic_Search.LLM import LLM_analys_Thread

from data.messagebox import critical_message, conclusion_question
from data.output_message import conclusion_rules_forming, conclusion_AI_output

from log.logging import logger
import numpy as np

class Semantic_search_main:
    def __init__(self, parent, db, level, model, top_window = None):
        self.top_window = top_window
        self.parent = parent
        self.db = db
        self.level = level
        self.model = model
        self.thread = None

    def start(self):
        self.vectorization_thread()

    def vectorization_thread(self):
        logger.info(f"SEARCH | STARTING... - {self.level} level")

        if self.level == "download":
            self.download_buttons_status(bool = False)
            filename = self.parent.gui.label_4.text()
            self.data = self.db.get_innovation_proposal_info(filename = filename)
            if self.data != None:
                self.thread = Vectorization_Thread(parent = self.parent, name = self.data[0], description = self.data[1], model = self.model)
                self.parent.gui.pushButton_2.setText("ВЕКТОРИЗАЦИЯ...")
                self.thread.vectorization_finished.connect(self.vectorization_finished)
                self.thread.vectorization_error.connect(self.vectorization_error)
                self.thread.start()
            else:
                pass

        elif self.level == "search":
            self.parent.gui.plainTextEdit_3.clear()

            db_embeddings_name = self.db.get_innovation_proposal_embeddings("name")
            db_embeddings_description = self.db.get_innovation_proposal_embeddings("description")
            db_embeddings_general = self.db.get_innovation_proposal_embeddings("general")

            text_name = self.parent.gui.plainTextEdit.toPlainText()
            text_description = self.parent.gui.plainTextEdit_2.toPlainText()

            if db_embeddings_name is not None and db_embeddings_description is not None and db_embeddings_general is not None:
                if len(text_name) == 0 and len(text_description) == 0:
                    logger.error("SEARCH | There is no one in the fields")
                    pass

                if len(text_name) > 0 and len(text_description) == 0:
                    logger.info("SEARCH | START - Name Searching...")
                    self.search_buttons_status(bool = False)

                elif len(text_description) > 0 and len(text_name) == 0:
                    logger.info("SEARCH | START - Description Searching...")
                    self.search_buttons_status(bool = False)

                elif len(text_name) > 0 and len(text_description) > 0:
                    logger.info("SEARCH | START - General Searching...")
                    self.search_buttons_status(bool = False)


                self.thread = Searching_Thread(self.parent, db_embeddings_name, db_embeddings_description, db_embeddings_general)
                self.thread.searching_finished.connect(self.searching_finished)
                self.thread.searching_error.connect(self.searching_error)
                self.thread.start()
            else:
                logger.error("Пустая база")
                pass
        
    def vectorization_finished(self, new_embedding):
        logger.info("SEARCH | FINISHED - Vectorization (SUCCESS)")
        self.thread.deleteLater()

        name = new_embedding[0]
        description = new_embedding[1]
        image = new_embedding[2]
        general = self.calculating_general(name, description)

        db_embeddings = self.db.get_innovation_proposal_embeddings("general")
        self.filename = self.parent.gui.label_4.text()
        self.db.add_innovation_proposal_embeddings(self.filename, name, description, general, image)
        if db_embeddings:
            self.semantic_deduplication_thread(general, db_embeddings)
        if db_embeddings == None:
            critical_message(self.parent, "Журнал пустой")
            self.parent.gui.pushButton_2.setText("Начать поиск")
            self.clear_fields()
            self.download_buttons_status(status = "SEARCH_END")

    def calculating_general(self, name, description):
        name_emb = np.array(name)
        desc_emb = np.array(description)
        
        name_emb = name_emb / np.linalg.norm(name_emb)
        desc_emb = desc_emb / np.linalg.norm(desc_emb)
        
        general_emb = (name_emb + desc_emb) / 2
        general_emb = general_emb / np.linalg.norm(general_emb)

        return general_emb

    def vectorization_error(self, error):
        logger.error(f"SEARCH | FINISHED - Vectorization (ERROR): {error}")
        self.thread.deleteLater()

    def semantic_deduplication_thread(self, general, db_embeddings):
        logger.info("SEARCH | START - Semantic deduplication")

        self.parent.gui.pushButton_2.setText("СЕМАНТИЧЕСКИЙ ПОИСК...")
        self.thread = Semantic_deduplication_Thread(general, db_embeddings)
        self.thread.semantic_deduplication_finished.connect(self.semantic_deduplication_finished)
        self.thread.semantic_deduplication_error.connect(self.semantic_deduplication_error)
        self.thread.start()
    
    def semantic_deduplication_finished(self, result):
        logger.info(f"SEARCH | FINISHED - Semantic deduplication (SUCCESS)\n\nНайдено {len(result)} похожих документов:")
        for i, item in enumerate(result, 1):
            logger.info(f"  {i}. {item['name']} - {item['similarity']:.4f} ({item['similarity']*100:.2f}%)")
        self.thread.deleteLater()

        response_text = conclusion_rules_forming(result, self.data[0])
        general = conclusion_AI_output(response_text, "Формируется...")
        self.parent.gui.plainTextEdit_2.setPlainText(general)
        self.LLM_analys(result)

    def semantic_deduplication_error(self, error):
        logger.error(f"SEARCH | FINISHED - Semantic deduplication (ERROR): {error}")
        self.thread.deleteLater()

    def searching_finished(self, result):
        logger.error(f"SEARCH | FINISHED - Semantic deduplication (SUCCESS)\n\nНайдено {len(result[0])} похожих документов:")
        for i, item in enumerate(result[0], 1):
            logger.info(f"  {i}. {item['name']} - {item['similarity']:.4f} ({item['similarity']*100:.2f}%)")
        self.thread.deleteLater()

        response_text = conclusion_rules_forming(result[0], result[1])
        general = conclusion_AI_output(response_text, "Формируется...")
        self.parent.gui.plainTextEdit_3.setPlainText(general)
        self.LLM_analys(result)
        
    def searching_error(self, error):
        logger.error(f"SEARCH | FINISHED - Semantic deduplication (ERROR): {error}")
        self.thread.deleteLater()

    def LLM_analys(self, result):
        logger.info(f"SEARCH | START - LLM Analys")

        if self.level == "download":
            self.parent.gui.pushButton_2.setText("АНАЛИЗ ЯЗЫКОВОЙ МОДЕЛИ...")
            self.thread = LLM_analys_Thread(self.db, result, self.data[0])

        elif self.level == "search":
            self.thread = LLM_analys_Thread(self.db, result[0], result[1])

        self.thread.LLM_analys_finished.connect(self.LLM_analys_finished)
        self.thread.LLM_analys_error.connect(self.LLM_analys_error)
        self.thread.start()

    def LLM_analys_finished(self, result):
        logger.info(f"SEARCH | FINISHED - LLM Analys (SUCCESS)")
        self.thread.deleteLater()

        if self.level == "download":
            general = conclusion_AI_output(result[0], result[1])
            self.new_proposal = result[2]
            self.parent.gui.plainTextEdit_2.setPlainText(general)
            self.parent.gui.pushButton_2.setText("Начать поиск")
            self.create_reply_conclusion()

        elif self.level == "search":
            general = conclusion_AI_output(result[0], result[1])
            self.parent.gui.plainTextEdit_3.setPlainText(general)
            self.search_buttons_status(bool = True)

        logger.info(f"SEARCH | SUCCESSFULL FINISHED")

    def LLM_analys_error(self, error):
        logger.info(f"SEARCH | FINISHED - LLM Analys (ERROR): {error}")
        self.thread.deleteLater()
        self.search_buttons_status(bool = True)

    def create_reply_conclusion(self):
        self.parent.gui.reply_pushButton = QPushButton(self.top_window)
        self.parent.gui.reply_pushButton.setGeometry(QtCore.QRect(910, 640, 171, 40))
        self.parent.gui.reply_pushButton.setText("Заключение")
        self.parent.gui.reply_pushButton.clicked.connect(self.user_conclusion)
        self.parent.gui.reply_pushButton.show()

    def user_conclusion(self):
        reply = conclusion_question(self.parent, "Признать рационализаторское предложение уникальным?", self.new_proposal[0])
        if reply == False:
            self.db.delete_innovation_proposal(self.filename[:-4])
        self.download_buttons_status(status = "USER_CONCLUSION")
        self.clear_fields()

    def download_buttons_status(self, bool = None, status = None):
        btn_group = [self.parent.gui.pushButton,
                     self.parent.gui.pushButton_2,
                     self.parent.gui.pushButton_3,
                     self.parent.gui.pushButton_4]

        if status == "SEARCH_END":
            for btn in btn_group:
                if btn == self.parent.gui.pushButton:
                    btn.setEnabled(True)
                else:
                    btn.setEnabled(False)
        elif status == "USER_CONCLUSION":
            self.parent.gui.reply_pushButton.hide()
            for btn in btn_group:
                if btn == self.parent.gui.pushButton:
                    btn.setEnabled(True)
                else:
                    btn.setEnabled(False)
        else:
            for btn in btn_group:
                btn.setEnabled(bool)

    def clear_fields(self):
        self.parent.gui.plainTextEdit.clear()
        self.parent.gui.plainTextEdit_2.clear()
        self.parent.gui.label_4.clear()

    def search_buttons_status(self, bool):
        self.parent.gui.pushButton.setEnabled(bool)
        self.parent.gui.pushButton_2.setEnabled(bool)