from handlers.engine.Text_Recognition.Recognition_main import Text_Recognition_main
import tempfile
import os

class Settings_logic:
    def __init__(self, parent, db, image_encoder_model, text_embedding_model):
        self.parent = parent
        self.db = db
        self.image_encoder_model = image_encoder_model
        self.text_embedding_model = text_embedding_model
        self.init_tmp()

    def init_tmp(self):
        tmp_dir = tempfile.gettempdir()
        self.tmp_path = os.path.join(tmp_dir, "ipc_tmp")
        os.makedirs(self.tmp_path, exist_ok = True)

    def load_data(self):
        self.load_process = Text_Recognition_main(parent = self.parent, db = self.db, level = "settings", image_encoder_model = self.image_encoder_model, text_embedding_model = self.text_embedding_model, tmp_path = self.tmp_path)
        self.load_process.start()

    def prompt_settings(self):
        self.parent.prompt.open()