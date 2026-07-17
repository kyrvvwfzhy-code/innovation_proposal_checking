from PyQt5.QtWidgets import QWidget
from gui.ui.search import Ui_Form
from handlers.hand_searching.hand_searching_main import Hand_searching_main

class Search_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.handlers()
        return self

    def handlers(self):
        self.hand_searching = Hand_searching_main(self, self.db)
        self.gui.pushButton_2.clicked.connect(self.hand_searching.start)
        #self.pushButton
