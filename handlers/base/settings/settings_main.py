from handlers.base.settings.settings_logic import Settings_logic

class Settings:
    def __init__(self, parent, db, image_encoder_model, text_embedding_model):
        self.parent = parent
        self.db = db
        self.image_encoder_model = image_encoder_model
        self.text_embedding_model = text_embedding_model
        self.logic = Settings_logic(self.parent, self.db, self.image_encoder_model, self.text_embedding_model)

    def download(self):
        self.logic.load_data()

    def prompt(self):
        self.logic.prompt_settings()
