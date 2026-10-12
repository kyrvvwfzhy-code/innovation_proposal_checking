from handlers.base.download.download_logic import Download_logic

class Download:
    def __init__(self, top_window, parent, db, image_encoder_model, text_embedding_model, instruct_model):
        self.top_window = top_window
        self.parent = parent
        self.db = db
        self.image_encoder_model = image_encoder_model
        self.text_embedding_model = text_embedding_model
        self.instruct_model = instruct_model
        self.logic = Download_logic(self.top_window, self.parent, self.db, self.image_encoder_model, self.text_embedding_model, self.instruct_model)
    
    def download(self):
        self.logic.recognition()

    def check(self):
        self.logic.searching()

    def edit(self):
        self.logic.change_data()

    # def write(self):
    #     self.logic.save_data()

    # def conclusion(self):
    #     self.logic.load_db()