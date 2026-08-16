from handlers.engine.ocr.ocr_main import OCR

class Settings_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def load_data(self):
        self.load_process = OCR(parent = self.parent, db = self.db, level = "settings")
        self.load_process.start()
        # self.parent.progressbar.open()

    def prompt_settings(self):
        self.parent.prompt.open()