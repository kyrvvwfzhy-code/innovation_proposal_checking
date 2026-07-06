from PyQt5.QtWidgets import QWidget
from gui.ui.settings import Ui_Form

from gui.prompt_window import Prompt_window
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
        self.prompt_window = Prompt_window(self.db)
        self.settings = Settings(self, self.db)
        self.gui.pushButton.clicked.connect(self.settings.load_data)
        self.gui.pushButton_2.clicked.connect(self.prompt_window.open)
