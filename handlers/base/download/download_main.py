from handlers.base.download.download_logic import Download_logic

class Download:
    def __init__(self, top_window, parent, db):
        self.top_window = top_window
        self.parent = parent
        self.db = db
        self.logic = Download_logic(self.top_window, self.parent, self.db)
    
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