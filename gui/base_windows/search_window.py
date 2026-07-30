from PyQt5.QtWidgets import QWidget

from gui.ui.search import Ui_Form

from handlers.search.search_main import Search

class Search_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals()
        return self

    def signals(self):
        self.handler = Search(self, self.db)
        self.gui.pushButton_2.clicked.connect(self.handler.search_by_text)
        self.gui.pushButton.clicked.connect(self.handler.search_by_image)

