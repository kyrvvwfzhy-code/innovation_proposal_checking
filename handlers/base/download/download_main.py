from handlers.base.download.download_logic import Download_logic

class Download:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.logic = Download_logic(self.parent, self.db)
    
    def download(self):
        self.logic.ocr()

    def check(self):
        self.logic.transformer()

    def edit(self):
        self.logic.change_data()
