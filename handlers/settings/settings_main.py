from handlers.settings.load_data.load_data_main import Load_data_main

class Settings:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
    
    def load_data(self):
        self.loading = Load_data_main(self.parent, self.db)
    
    def ollama(self):
        pass