from handlers.engine.Text_Recognition.Recognition_main import Text_Recognition_main
from handlers.engine.Semantic_Search.Search_main import Semantic_search_main

class Download_logic:
    def __init__(self, top_window, parent, db):
        self.top_window = top_window
        self.parent = parent
        self.db = db
        
    def recognition(self):
        self.recognition_process = Text_Recognition_main(parent = self.parent, db = self.db, level = "download", callback = self.recognition_finished)
        self.recognition_process.start()
        return 

    def searching(self):
        self.parent.gui.plainTextEdit_2.clear()
        self.searching_process = Semantic_search_main(top_window = self.top_window, parent = self.parent, db = self.db, level = "download")
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