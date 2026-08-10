from handlers.engine.transformer.transformer_main import Transformer

class Search_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def search_text(self):
        self.searching = Transformer(parent = self.parent, db = self.db, level = "search")
        self.searching.start()

    def search_image(self):
        pass
        # self.searching = Image_serching_main(self.parent, self.db)
        # self.searching.start()
    