from handlers.engine.ocr.ocr_main import OCR

class Progressbar_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
    def start_load(self):
        self.load = OCR(db = self.db, parent = self.parent, level = "settings")
        self.load.start()
