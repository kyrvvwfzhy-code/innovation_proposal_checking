from handlers.transformer.embedding import Embedding_Thread

class Embedding:
    def __init__(self, parent):
        self.parent = parent
        self.thread = None

    def start(self):
        self.embedding_thread()
    
    def embedding_thread(self):
        self.thread = Embedding_Thread(self.parent)
        self.parent.gui.pushButton_2.setEnabled(False)
        self.parent.gui.pushButton_2.setText("ВЕКТОРИЗАЦИЯ...")
        self.thread.embedding_finished.connect(self.embedding_finished)
        self.thread.embedding_error.connect(self.embedding_error)
        self.thread.start()
    
    def embedding_finished(self, result):
        self.parent.gui.pushButton_2.setEnabled(True)
        self.parent.gui.pushButton_2.setText("Начать проверку")
        self.parent.gui.plainTextEdit_2.setPlainText(str(result))
        self.thread.deleteLater()
    
    def embedding_error(self, error):
        print(f"erroremb - {error}")
        self.thread.deleteLater()


