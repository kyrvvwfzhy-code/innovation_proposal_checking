from handlers.options.progressbar.progressbar_logic import Progressbar_logic

class Progressbar:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.logic = Progressbar_logic(self.parent, self.db)
    
    def start(self):
        self.logic.start_load()
