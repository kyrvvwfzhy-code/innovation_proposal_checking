from handlers.auxiliary.hand_searching.hand_searching_main import Hand_searching_main
from handlers.auxiliary.image_searching.image_searching_main import Image_serching_main
class Search_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def search_text(self):
        self.searching = Hand_searching_main(self.parent, self.db)
        self.searching.start()

    def search_image(self):
        self.searching = Image_serching_main(self.parent, self.db)
        self.searching.start()
    