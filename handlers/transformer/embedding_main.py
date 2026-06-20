from handlers.transformer.embedding import Embedding_Thread

class Embedding:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None

    def start(self):
        self.embedding_thread()
    
    def embedding_thread(self):
        filename = self.parent.gui.label_4.text()
        name = self.db.get_name(filename)
        self.thread = Embedding_Thread(self.parent, name)
        self.parent.gui.pushButton_2.setEnabled(False)
        self.parent.gui.pushButton_2.setText("ВЕКТОРИЗАЦИЯ...")
        self.thread.embedding_finished.connect(self.embedding_finished)
        self.thread.embedding_error.connect(self.embedding_error)
        self.thread.start()
    
    def embedding_finished(self, embedding):
        self.parent.gui.pushButton_2.setEnabled(True)
        self.parent.gui.pushButton_2.setText("Начать проверку")
        self.parent.gui.plainTextEdit_2.setPlainText(str(embedding))
        filename = self.parent.gui.label_4.text()
        self.db.add_embedding(filename, embedding)
        self.thread.deleteLater()
    
    def embedding_error(self, error):
        print(f"erroremb - {error}")
        self.thread.deleteLater()


