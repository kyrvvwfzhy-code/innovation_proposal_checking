from handlers.base.search.search_logic import Search_logic

class Search:
    def __init__(self, parent, db, image_encoder_model, text_embedding_model, instruct_model):
        self.parent = parent
        self.db = db
        self.image_encoder_model = image_encoder_model
        self.text_embedding_model = text_embedding_model
        self.instruct_model = instruct_model
        self.logic = Search_logic(self.parent, self.db, self.image_encoder_model, self.text_embedding_model, self.instruct_model)

    def search_by_text(self):
        self.logic.search_text()

    def search_by_image(self):
        self.logic.search_image()
    
