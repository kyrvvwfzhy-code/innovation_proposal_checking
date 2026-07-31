from handlers.engine.hand_searching.searching import Searching_Thread

from handlers.engine.transformer.LLM import LLM_analys_Thread

from log.logging import logger

from data.data import make_response_text, general_text


class Hand_searching_main:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None

    def start(self):
        self.searching_thread()
    
    def searching_thread(self):
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
        self.db_prompt = self.db.get_innovation_proposal_prompt()
        self.thread = LLM_analys_Thread(result[0], result[1], self.db_prompt)
        self.thread.LLM_analys_finished.connect(self.LLM_analys_finished)
        self.thread.LLM_analys_error.connect(self.LLM_analys_error)
        self.thread.start()

    def LLM_analys_finished(self, result):
        general = general_text(result[0], result[1])
        self.parent.gui.plainTextEdit_3.setPlainText(general)
        self.parent.gui.pushButton_2.setEnabled(True)
        logger.info("LLM_analys is Ready")
        self.thread.deleteLater()
    
    def LLM_analys_error(self, error):
        logger.error(f"LLM_analys - {error}")
        self.thread.deleteLater()




