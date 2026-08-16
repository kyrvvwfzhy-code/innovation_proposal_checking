from handlers.engine.transformer.vectorization import Vectorization_Thread
from handlers.engine.transformer.semantic_deduplication import Semantic_deduplication_Thread
from handlers.engine.transformer.searching import Searching_Thread
from handlers.engine.transformer.LLM import LLM_analys_Thread

from data.messagebox import critical_message, question_message
from data.data import conclusion_forming, transformer_result

from log.logging import logger
import numpy as np

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
            logger.info(f"TRANSFORMER | STARTING... - {self.level} level")
            self.disable_buttons()
            filename = self.parent.gui.label_4.text()
            self.data = self.db.get_innovation_proposal_info(filename = filename)
            if self.data != None:
                self.thread = Vectorization_Thread(parent = self.parent, name = self.data[0], description = self.data[1])
                self.parent.gui.pushButton_2.setText("ВЕКТОРИЗАЦИЯ...")
                self.thread.vectorization_finished.connect(self.vectorization_finished)
                self.thread.vectorization_error.connect(self.vectorization_error)
                self.thread.start()
            else:
                pass
        elif self.level == "search":
            logger.info(f"TRANSFORMER | STARTING... - {self.level} level")
            self.parent.gui.pushButton0.setEnabled(False)

            db_embeddings_name = self.db.get_innovation_proposal_embeddings("name")
            db_embeddings_description = self.db.get_innovation_proposal_embeddings("description")
            db_embeddings_general = self.db.get_innovation_proposal_embeddings("general")
    
    
            if db_embeddings_name != None and db_embeddings_description != None:
                logger.info("TRANSFORMER | START - Search")

                self.thread = Searching_Thread(self.parent, db_embeddings_name, db_embeddings_description, db_embeddings_general)
                self.thread.searching_finished.connect(self.searching_finished)
                self.thread.searching_error.connect(self.searching_error)
                self.thread.start()
            else:
                pass
        
    def vectorization_finished(self, new_embedding):
        self.thread.deleteLater()
        logger.info("TRANSFORMER | FINISHED - Vectorization (SUCCESS)")
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
        logger.error(f"TRANSFORMER | FINISHED - Vectorization (ERROR): {error}")
        self.thread.deleteLater()

    def semantic_deduplication_thread(self, general, db_embeddings):
        logger.info("TRANSFORMER | START - Semantic deduplication")

        self.parent.gui.pushButton_2.setText("СЕМАНТИЧЕСКИЙ ПОИСК...")
        self.thread = Semantic_deduplication_Thread(general, db_embeddings)
        self.thread.semantic_deduplication_finished.connect(self.semantic_deduplication_finished)
        self.thread.semantic_deduplication_error.connect(self.semantic_deduplication_error)
        self.thread.start()
    
    def semantic_deduplication_finished(self, result):
        logger.error(f"TRANSFORMER | FINISHED - Semantic deduplication (SUCCESS)\n\nНайдено {len(result)} похожих документов:")
        for i, item in enumerate(result, 1):
            logger.info(f"  {i}. {item['name']} - {item['similarity']:.4f} ({item['similarity']*100:.2f}%)")
            
        self.thread.deleteLater()
        response_text = conclusion_forming(result, self.data[0])
        general = transformer_result(response_text, "Формируется...")
        self.parent.gui.plainTextEdit_2.setPlainText(general)
        self.LLM_analys(result)

    def semantic_deduplication_error(self, error):
        logger.error(f"TRANSFORMER | FINISHED - Semantic deduplication (ERROR): {error}")
        self.thread.deleteLater()

    def searching_finished(self, result):
        self.thread.deleteLater()
        logger.error(f"TRANSFORMER | FINISHED - Semantic deduplication (SUCCESS)\n\nНайдено {len(result[0])} похожих документов:")
        for i, item in enumerate(result[0], 1):
            logger.info(f"  {i}. {item['name']} - {item['similarity']:.4f} ({item['similarity']*100:.2f}%)")
        logger.info("SEARECHING is Ready")
        response_text = conclusion_forming(result[0], result[1])
        general = transformer_result(response_text, "Формируется...")
        self.parent.gui.plainTextEdit_3.setPlainText(general)
        self.LLM_analys(result)
        
    def searching_error(self, error):
        logger.error(f"TRANSFORMER | FINISHED - Semantic deduplication (ERROR): {error}")
        self.thread.deleteLater()

    def LLM_analys(self, result):
        logger.info(f"TRANSFORMER | START - LLM Analys")

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
        logger.info(f"TRANSFORMER | FINISHED - LLM Analys (SUCCESS)")

        if self.level == "download":
            self.enable_buttons()
            general = transformer_result(result[0], result[1])
            self.parent.gui.plainTextEdit_2.setPlainText(general)
            reply = question_message(self.parent, "Добавить в журнал", result[2])
            if reply == False:
                self.db.delete_innovation_proposal(self.filename[:-4])

            self.parent.gui.pushButton_2.setText("Начать поиск")
            self.thread.deleteLater()
        elif self.level == "search":
            general = transformer_result(result[0], result[1])
            self.parent.gui.plainTextEdit_3.setPlainText(general)
            self.parent.gui.pushButton_2.setEnabled(True)
            logger.info("LLM_analys is Ready")
            self.thread.deleteLater()
    
    def LLM_analys_error(self, error):
        logger.info(f"TRANSFORMER | FINISHED - LLM Analys (ERROR): {error}")

        if self.level == "download":
            print(f"errorllm - {error}")
            self.thread.deleteLater()
        elif self.level == "search":
            logger.error(f"LLM_analys - {error}")
            self.thread.deleteLater()

    def disable_buttons(self):
        self.parent.gui.pushButton.setEnabled(False)
        self.parent.gui.pushButton_2.setEnabled(False)
        self.parent.gui.pushButton_3.setEnabled(False)
        self.parent.gui.pushButton_4.setEnabled(False)

    def enable_buttons(self):
        self.parent.gui.pushButton.setEnabled(True)
        self.parent.gui.pushButton_2.setEnabled(True)
        self.parent.gui.pushButton_3.setEnabled(True)
        self.parent.gui.pushButton_4.setEnabled(True)