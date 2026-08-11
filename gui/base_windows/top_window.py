from PyQt5.QtWidgets import QWidget

from gui.ui.top import Ui_Form

from data.data import prompt_text

class Top_window(QWidget):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.init()

    def init(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.init_prompt()

    def init_prompt(self):
        exist = self.db.get_innovation_proposal_prompt()
        if exist == None:
            prompt = prompt_text("{conclution}")
            self.db.add_innovation_proposal_prompt(prompt)
        else:
            pass