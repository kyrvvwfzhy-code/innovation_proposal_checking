from PyQt5.QtWidgets import QWidget

from gui.ui.prompt import Ui_Form

from handlers.options.prompt.prompt_main import Prompt

class Prompt_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals()
        self.show()

    def signals(self):
        self.handler = Prompt(self, self.db)
        self.gui.pushButton.clicked.connect(self.handler.edit)
