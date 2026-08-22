from handlers.engine.Text_Recognition.Recognition_main import Text_Recognition_main

class Settings_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def load_data(self):
        self.load_process = Text_Recognition_main(parent = self.parent, db = self.db, level = "settings")
        self.load_process.start()

    def prompt_settings(self):
        self.parent.prompt.open()