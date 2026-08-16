from handlers.engine.transformer.transformer_main import Transformer

from handlers.engine.image_searching.image_searching_main import Image_searching

class Search_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def search_text(self):
        self.searching = Transformer(parent = self.parent, db = self.db, level = "search")
        self.searching.start()

    def search_image(self):
        self.searching = Image_searching(self.parent, self.db)
        self.searching.start()
    