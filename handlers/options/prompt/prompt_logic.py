class Prompt_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.init()

    def init(self):
        text = self.db.get_innovation_proposal_prompt()
        self.parent.gui.plainTextEdit.setPlainText(text)

    def change_prompt(self):
        new_prompt = self.parent.gui.plainTextEdit.toPlainText()
        self.db.update_innovation_proposal_prompt(new_prompt)
        self.parent.close()