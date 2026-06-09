from PyQt5 import QtWidgets

from GUI.gui import Ui_Form
from db.database import DataBase
from handlers.load_file import Load_file
from embedding.test import Embedding

class GUI_main:
    def __init__(self, parent):
        self.parent = parent
        self.init()
    
    def init(self):
        self.db = DataBase()
        self.db.create_tables()
        self.gui = Ui_Form()
        self.gui.setupUi(self.parent)
        self.handlers()
    
    def handlers(self):
        self.load = Load_file(self.parent)
        self.checking = Embedding(self.parent)
        self.gui.pushButton.clicked.connect(self.load.start)
        self.gui.pushButton_2.clicked.connect(self.checking.start)