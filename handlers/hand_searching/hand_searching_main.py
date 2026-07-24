from handlers.hand_searching.searching import Searching_Thread

from handlers.transformer.LLM import LLM_analys_Thread
from log.logging import logger

class Hand_searching_main:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None

    def start(self):
        self.searching_thread()
    
    def searching_thread(self):
        logger.info("START - hand_searching")
        db_embeddings = self.db.get_embeddings()
        if db_embeddings != None:
            self.thread = Searching_Thread(self.parent, db_embeddings)
            self.parent.gui.pushButton_2.setEnabled(False)
            self.thread.searching_finished.connect(self.searching_finished)
            self.thread.searching_error.connect(self.searching_error)
            self.thread.start()
        else:
            logger.debug(f"EMBEDDINGS TABLE - {len(db_embeddings)} records")
    
    def searching_finished(self, result):
        self.thread.deleteLater()
        logger.info("SEARECHING is Ready")
        self.LLM_analys(result)
    
    def searching_error(self, error):
        logger.error(f"SEARCHING - {error}")
        self.thread.deleteLater()
    
    def LLM_analys(self, result):
        self.result = result
        self.thread = LLM_analys_Thread(self.result[0], self.result[1], self.result[2])
        self.thread.LLM_analys_finished.connect(self.LLM_analys_finished)
        self.thread.LLM_analys_error.connect(self.LLM_analys_error)
        self.thread.start()

    def LLM_analys_finished(self, result):
        self.parent.gui.pushButton_2.setEnabled(True)
        self.parent.gui.plainTextEdit_3.setPlainText(result[0])
        logger.info("LLM_analys is Ready")
        self.thread.deleteLater()
    
    def LLM_analys_error(self, error):
        logger.error(f"LLM_analys - {error}")
        self.thread.deleteLater()




