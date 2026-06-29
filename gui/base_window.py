from PyQt5.QtWidgets import QWidget

from gui.ui.base import Ui_Form

from handlers.ocr.ocr_main import OCR_main
from handlers.transformer.transformer_main import Vectorization
from handlers.hand_searching.hand_searching_main import Hand_searching_main

class Base_window(QWidget):
    def __init__(self, parent, db):
        super().__init__()
        self.parent = parent
        self.db = db
        self.init()

    def init(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self.parent)
        self.handlers()

    def handlers(self):
        self.ocr = OCR_main(self.db, parent = self)
        self.checking = Vectorization(self, self.db)
        self.hand_searching = Hand_searching_main(self, self.db)
        self.gui.pushButton.clicked.connect(self.ocr.start)
        self.gui.pushButton_2.clicked.connect(self.checking.start)
        self.gui.pushButton_4.clicked.connect(self.hand_searching.start)
