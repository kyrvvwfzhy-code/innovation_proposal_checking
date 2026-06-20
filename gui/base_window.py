from PyQt5.QtWidgets import QWidget

from gui.ui.base import Ui_Form

from handlers.ocr.ocr_main import OCR_main
from handlers.transformer.embedding_main import Embedding

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
        self.checking = Embedding(self, self.db)
        self.gui.pushButton.clicked.connect(self.ocr.start)
        self.gui.pushButton_2.clicked.connect(self.checking.start)