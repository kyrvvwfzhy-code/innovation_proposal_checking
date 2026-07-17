from PyQt5.QtWidgets import QWidget

from gui.ui.progressbar import Ui_Form

from handlers.settings.settings_main import Settings

class Progressbar_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)

        self.settings = Settings(self, self.db)
        self.settings.load_data()
