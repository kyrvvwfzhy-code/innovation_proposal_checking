from PyQt5.QtWidgets import QWidget
from gui.ui.prompt import Ui_Form

class Prompt_window(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        prompt_text = self.db.get_prompt_text()
        self.gui.plainTextEdit.setPlainText(prompt_text)
        self.gui.pushButton.clicked.connect(self.update_prompt_text)
        self.show()

    def update_prompt_text(self):
        pass