from handlers.hand_searching.searching import Searching_Thread

from data.data import сhecking_result

class Hand_searching_main:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None

    def start(self):
        self.searching_thread()
    
    def searching_thread(self):
        db_embeddings = self.db.get_embeddings()
        if db_embeddings != None:
            self.thread = Searching_Thread(self.parent, db_embeddings)
            self.parent.gui.pushButton_4.setEnabled(False)
            self.thread.searching_finished.connect(self.searching_finished)
            self.thread.searching_error.connect(self.searching_error)
            self.thread.start()
        else:
            pass
    
    def searching_finished(self, result):
        text = сhecking_result(result[0], result[1])
        self.parent.gui.plainTextEdit_2.setPlainText(text)
        self.parent.gui.pushButton_4.setEnabled(True)
        self.thread.deleteLater()
    
    def searching_error(self, error):
        print(f"errorsearch - {error}")
        self.thread.deleteLater()





