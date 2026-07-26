class Prompt_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.init()

    def init(self):
        prompt_text = self.db.get_prompt_text()
        self.parent.gui.plainTextEdit.setPlainText(prompt_text)

    def change_prompt(self):
        pass