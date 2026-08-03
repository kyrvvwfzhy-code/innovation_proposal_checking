class Settings_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def load_data(self):
        self.parent.progressbar.open()

    def prompt_settings(self):
        self.parent.prompt.open()