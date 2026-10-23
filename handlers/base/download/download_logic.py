from handlers.engine.Text_Recognition.Recognition_main import Text_Recognition_main
from handlers.engine.Semantic_Search.Search_main import Semantic_search_main
import tempfile
import os

class Download_logic:
    def __init__(self, top_window, parent, db, image_encoder_model, text_embedding_model, instruct_model):
        self.top_window = top_window
        self.parent = parent
        self.db = db
        self.image_encoder_model = image_encoder_model
        self.text_embedding_model = text_embedding_model
        self.instruct_model = instruct_model
        self.init_tmp()

    def init_tmp(self):
        tmp_dir = tempfile.gettempdir()
        self.tmp_path = os.path.join(tmp_dir, "ipc_tmp")
        os.makedirs(self.tmp_path, exist_ok = True)
        
    def recognition(self):
        self.recognition_process = Text_Recognition_main(parent = self.parent, db = self.db, level = "download", callback = self.recognition_finished, text_embedding_model = self.text_embedding_model, tmp_path = self.tmp_path, image_encoder_model = None)
        self.recognition_process.start()
        return 

    def searching(self):
        self.parent.gui.textBrowser_2.clear()
        self.searching_process = Semantic_search_main(parent = self.parent, db = self.db, level = "download", image_encoder_model = self.image_encoder_model, text_embedding_model = self.text_embedding_model, instruct_model = self.instruct_model, top_window = self.top_window, tmp_path = self.tmp_path)
        self.searching_process.start()

    def change_data(self):
        self.parent.edit.open(self.db, self.filename, self.registered, self.name, self.description)

    # def save_data(self):
    #   pass

    # def load_db(self):
    #     pass

    def recognition_finished(self, filename, registered, name, description):
        self.parent.gui.pushButton_3.setEnabled(True)
        self.filename = filename
        self.registered = registered
        self.name = name
        self.description = description
        self.change_data()
        return self.filename, self.registered, self.name, self.description