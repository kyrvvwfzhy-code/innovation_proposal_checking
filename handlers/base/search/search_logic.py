from handlers.engine.Semantic_Search.Search_main import Semantic_search_main
from handlers.engine.Image_Searching.Searching_main import Image_searching_main

class Search_logic:
    def __init__(self, parent, db, image_encoder_model, text_embedding_model, instruct_model):
        self.parent = parent
        self.db = db
        self.image_encoder_model = image_encoder_model
        self.text_embedding_model = text_embedding_model
        self.instruct_model = instruct_model

    def search_text(self):
        self.searching = Semantic_search_main(parent = self.parent, db = self.db, level = "search", text_embedding_model = self.text_embedding_model, instruct_model = self.instruct_model, image_encoder_model = None)
        self.searching.start()

    def search_image(self):
        self.searching = Image_searching_main(self.parent, self.db, self.image_encoder_model)
        self.searching.start()
    