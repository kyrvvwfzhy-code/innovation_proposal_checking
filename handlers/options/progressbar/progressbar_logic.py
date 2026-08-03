from handlers.auxiliary.load_data.load_data_main import Load_data_main

class Progressbar_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
    def start_load(self):
        self.load = Load_data_main(self.parent, self.db)
        self.load.start()
