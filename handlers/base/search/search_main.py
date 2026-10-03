from handlers.base.search.search_logic import Search_logic

class Search:
    def __init__(self, parent, db, model):
        self.parent = parent
        self.db = db
        self.model = model
        self.logic = Search_logic(self.parent, self.db, self.model)

    def search_by_text(self):
        self.logic.search_text()

    def search_by_image(self):
        self.logic.search_image()
    
