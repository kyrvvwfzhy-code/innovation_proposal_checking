from PyQt5.QtWidgets import QWidget
from gui.ui.base import Ui_Form
from handlers.ocr.ocr_main import OCR_main
from handlers.transformer.transformer_main import Vectorization

class Base_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.handlers()
        return self
    
    def handlers(self):
        self.ocr = OCR_main(self.db, parent = self)
        self.checking = Vectorization(self, self.db)
        self.gui.pushButton.clicked.connect(self.ocr.start)
        self.gui.pushButton_2.clicked.connect(self.checking.start)
