from PyQt5.QtWidgets import QWidget

from gui.ui.download import Ui_Form
from gui.option_windows.edit_window import Edit_window

from handlers.download.download_main import Download

class Download_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals()
        return self
    
    def signals(self):
        self.handler = Download(self.db, parent = self)
        self.edit = Edit_window()
        self.gui.pushButton.clicked.connect(self.handler.download)
        self.gui.pushButton_2.clicked.connect(self.handler.check)


