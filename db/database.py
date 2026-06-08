import sqlite3
import threading

db = sqlite3.connect("RPC.db")
cursor = db.cursor()

class DataBase:
    def __init__(self, db_path="RPC.db"):
        self.db_path = db_path
        self._local = threading.local()

    def _get_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path)
            self._local.cursor = self._local.connection.cursor()
        return self._local.connection, self._local.cursor

    def create_tables(self):
        conn, cursor = self._get_connection()
        cursor.execute("""CREATE TABLE IF NOT EXISTS rational_proposal (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT UNIQUE,
                       path TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )""")
    
    def add_rational_proposal(self, name, path):
        conn, cursor = self._get_connection()

        try:
            cursor.execute("INSERT INTO rational_proposal (name, path) VALUES (?, ?)",
                        (name, path))
            conn.commit()
        except sqlite3.IntegrityError:
            error = "Данный документ уже выгружен"
            return error
    
    def get_loaded_rp(self, name):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("SELECT path FROM rational_proposal WHERE name = (?)",
                           (name,))
            path = cursor.fetchone()
            return path
        except Exception as e:
            print(f"Error {e}")

if __name__ == "__main__":
    start = DataBase()
    # start.create_tables()
    start.get_loaded_rp()