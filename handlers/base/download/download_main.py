from handlers.base.download.download_logic import Download_logic

class Download:
    def __init__(self, db, parent):
        self.db = db
        self.parent = parent
        self.logic = Download_logic(self.db, self.parent)
    
    def download(self):
        self.logic.ocr()

    def check(self):
        self.logic.transformer()

    def edit(self):
        self.logic.change_data()

    def save(self):
        self.logic.save_data()