from PyQt5.QtWidgets import QWidget
from gui.ui.settings import Ui_Form
from gui.prompt_window import Prompt_window
from gui.progressbar_window import Progressbar_window

class Settings_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.settings_window()
        return self
    
    def settings_window(self):
        self.progressbar = Progressbar_window(self.db)
        self.gui.pushButton.clicked.connect(self.progressbar.open)
        self.prompt_window = Prompt_window(self.db)
        self.gui.pushButton_2.clicked.connect(self.prompt_window.open)
