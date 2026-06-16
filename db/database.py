import sqlite3
import threading

db = sqlite3.connect("IPC.db")
cursor = db.cursor()

class DataBase:
    def __init__(self, db_path="IPC.db"):
        self.db_path = db_path
        self._local = threading.local()

    def _get_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path)
            self._local.cursor = self._local.connection.cursor()
        return self._local.connection, self._local.cursor

    def create_tables(self):
        conn, cursor = self._get_connection()
        cursor.execute("""CREATE TABLE IF NOT EXISTS innovation_proposal (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       filename TEXT UNIQUE,
                       path TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS key_information (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       innovation_proposal_id,
                       registered TEXT,
                       name TEXT,
                       author TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (innovation_proposal_id) REFERENCES innovation_proposal (id)
                       )""")
        conn.commit()

#--------------------------------------------innovation_proposal--------------------------------------------
    def add_innovation_proposal(self, filename, path):
        conn, cursor = self._get_connection()

        try:
            cursor.execute("INSERT INTO innovation_proposal (filename, path) VALUES (?, ?)",
                        (filename, path))
            conn.commit()
        except sqlite3.IntegrityError:
            error = "Данный документ уже выгружен"
            return error
    
    def get_loaded_ip(self, filename):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("SELECT path FROM innovation_proposal WHERE filename = (?)",
                           (filename,))
            path = cursor.fetchone()
            return path
        except Exception as e:
            print(f"Error {e}")

#--------------------------------------------key_information--------------------------------------------
    
    def add_key_information(self, registered, name, author):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("INSERT INTO key_information (registered, name, author) VALUES (?, ?, ?)",
                           (registered, name, author))
            conn.commit()
        except Exception as e:
            print(f"Error {e}")
    
    def get_key_information(self):
        conn, cursor = self._get_connection()
        try:
            result = cursor.execute("SELECT id, registered, name, author FROM key_information")
            data = result.fetchall()
            return data
        except Exception as e:
            print(f"Eror {e}")

if __name__ == "__main__":
    start = DataBase()
    # start.create_tables()
    start.get_loaded_rp()