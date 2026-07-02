import sqlite3
import threading
import numpy as np

class DataBase:
    def __init__(self, db_path="IPC.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(
            self.db_path,
            timeout=10,  
            check_same_thread=False
        )
        #self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def _get_connection(self):
        return self.connection, self.cursor

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
                       innovation_proposal_id INTEGER,
                       number TEXT,
                       date TEXT,
                       name TEXT UNIQUE,
                       author TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (innovation_proposal_id) REFERENCES innovation_proposal (id)
                       )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS embeddings (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       innovation_proposal_id INTEGER,
                       name TEXT UNIQUE,
                       embedding BLOB NOT NULL,
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
    
    def delete_ip(self, filename):
        conn, cursor = self._get_connection()
        try:
            result = cursor.execute("SELECT id FROM innovation_proposal WHERE filename = (?)",
                           (filename,))
            if result:
                id = result.fetchone()
                
            cursor.execute("DELETE FROM key_information WHERE id = (?)",
                           (id[0],))
            cursor.execute("DELETE FROM innovation_proposal WHERE id = (?)",
                           (id[0],))
            cursor.execute("DELETE FROM embeddings WHERE id = (?)",
                           (id[0],))
            conn.commit()
        except Exception as e:
            print(f"Error {e}")

#--------------------------------------------key_information--------------------------------------------
    
    def add_key_information(self, filename, number, date, name, author):
        conn, cursor = self._get_connection()
        try:
            id = cursor.execute("SELECT id FROM innovation_proposal WHERE filename = ?", (filename,))
            
            if id:
                id = id.fetchone()
            
            cursor.execute("""INSERT INTO key_information 
                        (innovation_proposal_id, number, date, name, author) 
                        VALUES (?, ?, ?, ?, ?)""",
                        (id[0], number, date, name, author))
            conn.commit()
            
        except Exception as e:
            print(f"Error in add_key_information: {e}")
    
    def get_key_information(self):
        conn, cursor = self._get_connection()
        try:
            result = cursor.execute("""SELECT innovation_proposal.filename,
                                    key_information.number,
                                    key_information.date,
                                    key_information.name, 
                                    key_information.author
                                    FROM innovation_proposal
                                    LEFT JOIN key_information ON innovation_proposal.id = key_information.innovation_proposal_id
                                    """)
            data = result.fetchall()
            return data
        except Exception as e:
            print(f"Eror {e}")
    
    def get_name(self, filename):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""SELECT key_information.name
                                    FROM innovation_proposal
                                    LEFT JOIN key_information ON innovation_proposal.id = key_information.innovation_proposal_id
                                    WHERE innovation_proposal.filename = ?""",
                                    (filename[:-4],))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error {e}")

#--------------------------------------------key_information--------------------------------------------

    def add_embedding(self, filename, embedding):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""SELECT innovation_proposal.id,
                                    key_information.name
                                    FROM innovation_proposal
                                    LEFT JOIN key_information ON innovation_proposal.id = key_information.innovation_proposal_id
                                    WHERE innovation_proposal.filename = ?""",
                                    (filename[:-4],))
            result = cursor.fetchone()
    
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            cursor.execute("INSERT OR IGNORE INTO embeddings (innovation_proposal_id, name, embedding) VALUES (?, ?, ?)",
                               (result[0], result[1], embedding_bytes))
            conn.commit()
        except Exception as e:
            print(f"Error {e}")
    
    def get_embeddings(self):
        conn, cursor = self._get_connection()
        try:
            result = cursor.execute("SELECT name, embedding FROM embeddings")
            embedding_list = []
            for i in result.fetchall():
                name = i[0]
                embedding_bytes = i[1]
                embedding_numpy = np.frombuffer(embedding_bytes, dtype=np.float32)
                embedding_list.append([name, embedding_numpy])
            
            if embedding_list == []:
                return None
            else:
                return embedding_list

        except Exception as e:
            print(f"Error {e}")
    
    def delete_embeddings(self, filename):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""SELECT key_information.name
                                    FROM innovation_proposal
                                    LEFT JOIN key_information ON innovation_proposal.id = key_information.innovation_proposal_id
                                    WHERE innovation_proposal.filename = ?""",
                                    (filename[:-4],))
            result = cursor.fetchone()
            
            id = cursor.execute("SELECT innovation_proposal_id FROM embeddings WHERE name = ?",
                                (result[0],))
            if id:
                id = id.fetchone()
                
            cursor.execute("DELETE FROM key_information WHERE id = (?)",
                           (id[0],))
            cursor.execute("DELETE FROM innovation_proposal WHERE id = (?)",
                           (id[0],))
            cursor.execute("DELETE FROM embeddings WHERE name = ?",
                               (result[0],))
            conn.commit()
        except Exception as e:
            print(f"Error {e}")

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    start = DataBase()
    # start.create_tables()
    start.get_loaded_rp()