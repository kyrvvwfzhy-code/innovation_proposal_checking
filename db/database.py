import sqlite3

db = sqlite3.connect("RPC.db")
cursor = db.cursor()

class DataBase:
    def create_tables(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS rational_proposal (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT UNIQUE,
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
        try:
            cursor.execute("INSERT INTO rational_proposal (name, path) VALUES (?, ?)",
                        (name, path))
            db.commit()
        except sqlite3.IntegrityError:
            error = "Данный документ уже выгружен"
            return error

    
    def get_loaded_rp(self):
        try:
            cursor.execute("SELECT name, path FROM rational_proposal")
            path = cursor.fetchone()
            return path
        except Exception as e:
            print(f"Error {e}")



if __name__ == "__main__":
    start = DataBase()
    start.create_tables()