from handlers.base.journal.journal_logic import Journal_logic

class Journal:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.logic = Journal_logic(self.parent, self.db)

    def delete(self):
        self.logic.delete_selected()
    
    def save(self):
        self.logic.save_changes()
    
    def update(self):
        self.logic.update_table(self.logic)

    def search(self):
        self.logic.search_record()
     

