from handlers.engine.Text_Recognition.Recognition_main import Text_Recognition_main

class Settings_logic:
    def __init__(self, parent, db, model):
        self.parent = parent
        self.db = db
        self.model = model

    def load_data(self):
        self.load_process = Text_Recognition_main(parent = self.parent, db = self.db, level = "settings", model = self.model)
        self.load_process.start()

    def prompt_settings(self):
        self.parent.prompt.open()