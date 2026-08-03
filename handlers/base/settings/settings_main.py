from handlers.base.settings.settings_logic import Settings_logic

class Settings:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db 
        self.logic = Settings_logic(self.parent, self.db)

    def download(self):
        self.logic.load_data()

    def prompt(self):
        self.logic.prompt_settings()
