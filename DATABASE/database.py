import sqlite3

db = sqlite3.connect("RPC.db")
cursor = db.cursor()

class DataBase:
    def create_tables(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS rational_proposal (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       path TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )""")
                       
        cursor.execute("""CREATE TABLE IF NOT EXISTS load (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       rational_proposal_id INTEGER,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (rational_proposal_id) REFERENCES rational_proposal(id) ON DELETE CASCADE
                       )""")
        
        db.commit()
    
    def add_rational_proposal(self, name, path):
        cursor.execute("INSERT INTO rational_proposal (name, path) VALUES (?, ?)",
                       (name, path))
        db.commit()
    
    def get_

if __name__ == "__main__":
    start = DataBase()
    start.create_tables()