from handlers.engine.ocr.ocr_main import OCR
from handlers.engine.transformer.transformer_main import Transformer

class Download_logic:
    def __init__(self, db, parent):
        self.db = db
        self.parent = parent
        
    def ocr(self):
        self.ocr_process = OCR(db = self.db, parent = self.parent, level = "download", callback = self.on_ocr_finished)
        self.ocr_process.start()
        return 

    def transformer(self):
        self.parent.gui.plainTextEdit_2.clear()
        self.check = Transformer(parent = self.parent, db = self.db, level = "download")
        self.check.start()

    def on_ocr_finished(self, filename, registered, name, description):
        self.parent.gui.pushButton_3.setEnabled(True)
        self.filename = filename
        self.registered = registered
        self.name = name
        self.description = description
        self.change_data()

        return self.filename, self.registered, self.name, self.description

    def change_data(self):
        self.parent.edit.open(self.db, self.filename, self.registered, self.name, self.description)
        
    def save_data(self):
        pass