from PyQt5.QtWidgets import QWidget

from gui.ui.base import Ui_Form

from handlers.load_file_handler import Load_file
from handlers.transformer.embedding import Embedding 

class Base_window(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init()

    def init(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self.parent)
        self.handlers()

    def handlers(self):
        self.load = Load_file(self)
        self.checking = Embedding(self)
        self.gui.pushButton.clicked.connect(self.load.start)
        self.gui.pushButton_2.clicked.connect(self.checking.start)