from PyQt5.QtWidgets import QWidget
from gui.ui.settings import Ui_Form

from handlers.settings.settings_main import Settings

class Settings_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.settings_window()
        self.show()
    
    def settings_window(self):
        self.settings = Settings(self, self.db)
        self.gui.pushButton.clicked.connect(self.settings.main)
