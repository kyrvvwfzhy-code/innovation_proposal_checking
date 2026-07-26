from handlers.engine.hand_searching.hand_searching_main import Hand_searching_main

class Search_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def search(self):
        self.searching = Hand_searching_main(self.parent, self.db)
        self.searching.start()