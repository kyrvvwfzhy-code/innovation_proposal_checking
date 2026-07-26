from handlers.engine.ocr.ocr_main import OCR_main
from handlers.engine.transformer.transformer_main import Vectorization

class Download_logic:
    def __init__(self, db, parent):
        self.db = db
        self.parent = parent
        
    def ocr(self):
        self.ocr_process = OCR_main(self.db, parent = self.parent)
        self.ocr_process.start()

    def transformer(self):
        self.check = Vectorization(self.parent, self.db)
        self.check.start()