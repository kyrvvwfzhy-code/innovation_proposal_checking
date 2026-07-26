from PyQt5.QtWidgets import QWidget

from gui.ui.progressbar import Ui_Form

from handlers.options.progressbar.progressbar_main import Progressbar

class Progressbar_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals()

    def signals(self):
        self.handler = Progressbar(self, self.db)
        self.handler.start()
