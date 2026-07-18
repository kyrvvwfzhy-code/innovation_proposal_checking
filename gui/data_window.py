from PyQt5.QtWidgets import QWidget
from gui.ui.data import Ui_Form
from handlers.data_journal.loaded_documents import Loaded_documents
from log.logging import logger

class Data_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.loaded_documents = None

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.data_window()
        self.gui.pushButton_3.clicked.connect(self.update_table)
        return self
    
    def data_window(self):
        self.loaded_documents = Loaded_documents(self, self.db)
        #self.pushButton_2
    
    def update_table(self):
            if self.loaded_documents is not None:
                if hasattr(self.loaded_documents, 'table'):
                    self.loaded_documents.table.setRowCount(0)
                    data = self.db.get_key_information()
                    if data:
                        self.loaded_documents.add_data(data)
                    logger.info("✅ Таблица обновлена")
                    return