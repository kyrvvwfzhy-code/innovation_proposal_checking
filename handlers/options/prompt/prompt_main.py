from handlers.options.prompt.prompt_logic import Prompt_logic

class Prompt:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.logic = Prompt_logic(self.parent, self.db)

    def edit(self):
        self.logic.change_prompt()