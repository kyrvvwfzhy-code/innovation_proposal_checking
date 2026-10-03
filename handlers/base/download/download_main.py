from handlers.base.download.download_logic import Download_logic

class Download:
    def __init__(self, top_window, parent, db, model):
        self.top_window = top_window
        self.parent = parent
        self.db = db
        self.model = model
        self.logic = Download_logic(self.top_window, self.parent, self.db, self.model)
    
    def download(self):
        self.logic.recognition()

    def check(self):
        self.logic.searching()

    def edit(self):
        self.logic.change_data()

    # def write(self):
    #     self.logic.save_data()

    # def conclusion(self):
    #     self.logic.load_db()