from handlers.base.settings.settings_logic import Settings_logic

class Settings:
    def __init__(self, parent, db, model):
        self.parent = parent
        self.db = db
        self.model = model
        self.logic = Settings_logic(self.parent, self.db, self.model)

    def download(self):
        self.logic.load_data()

    def prompt(self):
        self.logic.prompt_settings()
