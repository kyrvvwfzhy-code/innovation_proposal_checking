from PyQt5.QtWidgets import QWidget

from gui.ui.top import Ui_Form

from data.LLM_prompt import default_prompt

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
            prompt = default_prompt("{conclution}")
            self.db.add_innovation_proposal_prompt(prompt)
        else:
            pass