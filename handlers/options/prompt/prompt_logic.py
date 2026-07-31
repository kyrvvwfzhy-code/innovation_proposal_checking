from data.data import prompt_text

class Prompt_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.init()

    def init(self):
        prompt = prompt_text()
        exist = self.db.get_innovation_proposal_prompt()
        if exist == None:
            self.db.add_innovation_proposal_prompt(prompt)
        text = self.db.get_innovation_proposal_prompt()
        self.parent.gui.plainTextEdit.setPlainText(text)

    def change_prompt(self):
        new_prompt = self.parent.gui.plainTextEdit.toPlainText()
        self.db.update_get_innovation_proposal_prompt_prompt(new_prompt)
        self.parent.close()