from handlers.engine.load_data.load_data_main import Load_data_main

class Settings_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def load_data(self):
        self.parent.progressbar.open()

    def prompt_settings(self):
        self.parent.prompt.open()