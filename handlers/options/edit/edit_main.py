from handlers.options.edit.edit_logic import Edit_logic

class Edit:
    def __init__(self, parent, db, filename, registered, name, description):
        self.parent = parent
        self.db = db
        self.filename = filename
        self.registered = registered
        self.name = name
        
        self.logic = Edit_logic(parent, db, filename, registered, name, description)