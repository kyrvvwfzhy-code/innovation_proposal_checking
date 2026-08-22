from handlers.engine.Semantic_Search.Search_main import Semantic_search_main

from handlers.engine.Image_Searching.Searching_main import Image_searching_main

class Search_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def search_text(self):
        self.searching = Semantic_search_main(parent = self.parent, db = self.db, level = "search")
        self.searching.start()

    def search_image(self):
        self.searching = Image_searching_main(self.parent, self.db)
        self.searching.start()
    