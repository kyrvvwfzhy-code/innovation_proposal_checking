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
                       registered TEXT,
                       name TEXT UNIQUE,
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

        cursor.execute("""CREATE TABLE IF NOT EXISTS prompt_text (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       prompt TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )""")
        conn.commit()

#--------------------------------------------tmp---------------------------------------------------------


        
#--------------------------------------------innovation_proposal--------------------------------------------
    def add_innovation_proposal(self, filename, path):
        conn, cursor = self._get_connection()

        try:
            cursor.execute("INSERT INTO innovation_proposal (filename, path) VALUES (?, ?)",
                        (filename, path))
            conn.commit()
        except sqlite3.IntegrityError as IntegrityError:
            return IntegrityError
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
    def get_loaded_ip(self, filename):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("SELECT path FROM innovation_proposal WHERE filename = (?)",
                           (filename,))
            path = cursor.fetchone()
            return path
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
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
            return f"DATABASE ERROR - {e}"

#--------------------------------------------key_information--------------------------------------------
    
    def add_key_information(self, filename, registered, name):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""INSERT INTO key_information (innovation_proposal_id, registered, name)
                           SELECT id, ?, ? FROM innovation_proposal
                           WHERE filename = ?
                           """, (registered, name, filename))
            conn.commit()
    
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
    def get_key_information(self):
        conn, cursor = self._get_connection()
        try:
            result = cursor.execute("""SELECT innovation_proposal.filename,
                                    key_information.registered,
                                    key_information.name
                                    FROM innovation_proposal
                                    LEFT JOIN key_information ON innovation_proposal.id = key_information.innovation_proposal_id
                                    """)
            data = result.fetchall()
            return data
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
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
            return f"DATABASE ERROR - {e}"
    
    def update_data(self, filename, new_registered, new_name):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""SELECT registered, name FROM key_information 
                        WHERE innovation_proposal_id = (
                            SELECT id FROM innovation_proposal WHERE filename = ?
                        )
                        """, (filename,))
            old_data = cursor.fetchone()
            
            if not old_data:
                return 0
            
            old_registered, old_name = old_data
            
            if old_registered == new_registered and old_name == new_name:
                return 0

            cursor.execute("""UPDATE key_information SET registered = ?, name = ?
                        WHERE innovation_proposal_id = (
                            SELECT id FROM innovation_proposal WHERE filename = ?
                        )
                        """, (new_registered, new_name, filename))
            conn.commit()
            return cursor.rowcount
            
        except Exception as e:
            print(f"Ошибка обновления: {e}")
            return 0

#--------------------------------------------embeddings--------------------------------------------

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
            return f"DATABASE ERROR - {e}"
    
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
            return f"DATABASE ERROR - {e}"
    
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
            return f"DATABASE ERROR - {e}"
    
    def update_embedding(self, filename, embedding):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""SELECT innovation_proposal.id,
                                    key_information.name
                                    FROM innovation_proposal
                                    LEFT JOIN key_information ON innovation_proposal.id = key_information.innovation_proposal_id
                                    WHERE innovation_proposal.filename = ?""",
                                    (filename,))
            result = cursor.fetchone()
    
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            cursor.execute("""UPDATE embeddings 
                            SET innovation_proposal_id = ?, name = ?, embedding = ?
                            WHERE innovation_proposal_id = ?""",
                        (result[0], result[1], embedding_bytes, result[0]))
            conn.commit()

        except Exception as e:
            return f"DATABASE ERROR - {e}"

#--------------------------------------------prompt_text--------------------------------------------

    def add_prompt_text(self, prompt):
            conn, cursor = self._get_connection()

            try:
                cursor.execute("INSERT INTO prompt_text prompt VALUES ?",
                            (prompt,))
                conn.commit()
            except Exception as e:
                return f"DATABASE ERROR - {e}"
    
    def update_prompt_text(self, new_prompt):
            conn, cursor = self._get_connection()

            try:
                cursor.execute("UPDATE prompt_text SET prompt = ? WHERE id = 1",
                            (new_prompt,))
                conn.commit()
            except Exception as e:
                return f"DATABASE ERROR - {e}"
    
    def get_prompt_text(self):
            conn, cursor = self._get_connection()

            try:
                cursor.execute("SELECT prompt INTO prompt_text WHERE id = 1")

                prompt_text = cursor.fetchone()
                return prompt_text[0]
            except Exception as e:
                return f"DATABASE ERROR - {e}"

#--------------------------------------------DB_CLOSE--------------------------------------------

    def close(self):
        self.connection.close()
