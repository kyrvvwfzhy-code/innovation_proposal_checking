from PyQt5.QtWidgets import QWidget

from gui.ui.data import Ui_Form
from handlers.data_journal.loaded_documents import Loaded_documents

class Data_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.data_window()
        self.show()
    
    def data_window(self):
        self.loaded_documents = Loaded_documents(self, self.db)