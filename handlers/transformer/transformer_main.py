from PyQt5.QtWidgets import QMessageBox
from handlers.transformer.vectorization import Vectorization_Thread
from handlers.transformer.semantic_deduplication import Semantic_deduplication_Thread

from handlers.transformer.LLM import LLM_analys_Thread

class Vectorization:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None

    def start(self):
        self.vectorization_thread()
    
    def vectorization_thread(self):
        filename = self.parent.gui.label_4.text()
        self.name = self.db.get_name(filename)
        if self.name != None:
            self.thread = Vectorization_Thread(self.parent, self.name)
            self.parent.gui.pushButton_2.setEnabled(False)
            self.parent.gui.pushButton_2.setText("ВЕКТОРИЗАЦИЯ...")
            self.thread.vectorization_finished.connect(self.vectorization_finished)
            self.thread.vectorization_error.connect(self.vectorization_error)
            self.thread.start()
        else:
            pass
    
    def vectorization_finished(self, new_embedding):
        self.thread.deleteLater()
        db_embeddings = self.db.get_embeddings()
        if db_embeddings:
            self.semantic_deduplication_thread(new_embedding, db_embeddings)
        if db_embeddings == None:
            message = "БД Эмбеддингов пустая"
            self.parent.gui.pushButton_2.setEnabled(True)
            self.parent.gui.pushButton_2.setText("Начать поиск")
            QMessageBox.information(self.parent, "Информация", message)
        self.filename = self.parent.gui.label_4.text()
        self.db.add_embedding(self.filename, new_embedding)
            
    def vectorization_error(self, error):
        print(f"erroremb - {error}")
        self.thread.deleteLater()

    def semantic_deduplication_thread(self, new_embedding, db_embeddings):
        self.parent.gui.pushButton_2.setText("СЕМАНТИЧЕСКИЙ ПОИСК...")
        self.thread = Semantic_deduplication_Thread(new_embedding, db_embeddings)
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
        self.thread = LLM_analys_Thread(result[0], result[1], self.name)
        self.thread.LLM_analys_finished.connect(self.LLM_analys_finished)
        self.thread.LLM_analys_error.connect(self.LLM_analys_error)
        self.thread.start()

    def LLM_analys_finished(self, result, analys):
        self.parent.gui.plainTextEdit_2.setPlainText(analys)
        reply = QMessageBox.question(
            self.parent,
            "Подтверждение уникальности",
            f"Добавить в базу\"{result[1]}\"?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.No:
            self.db.delete_embeddings(self.filename)
        self.parent.gui.pushButton_2.setEnabled(True)
        self.parent.gui.pushButton_2.setText("Начать поиск")
        self.thread.deleteLater()
    
    def LLM_analys_error(self, error):
        print(f"errorllm - {error}")
        self.thread.deleteLater()

