from PyQt5.QtWidgets import QWidget

from gui.ui.journal import Ui_Form

from handlers.base.journal.journal_main import Journal

class Journal_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals()
        return self
    
    def signals(self):
        self.handler = Journal(self, self.db)
        self.gui.pushButton.clicked.connect(self.handler.delete)
        self.gui.pushButton_2.clicked.connect(self.handler.save)
        self.gui.pushButton_3.clicked.connect(self.handler.update)
        self.gui.lineEdit.returnPressed.connect(self.handler.search)

        
