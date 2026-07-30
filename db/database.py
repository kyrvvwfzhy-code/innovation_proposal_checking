import sqlite3
import numpy as np

class DataBase:
    def __init__(self, db_path="IPC.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(
            self.db_path,
            timeout=10,  
            check_same_thread=False
        )
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()
        

    def _get_connection(self):
        return self.connection, self.cursor

    def create_tables(self):
        conn, cursor = self._get_connection()

#--------------------------------------------create_tables--------------------------------------------

        cursor.execute("""CREATE TABLE IF NOT EXISTS innovation_proposal (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       filename TEXT UNIQUE,
                       filepath TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS innovation_proposal_info (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       innovation_proposal_id INTEGER,
                       registered TEXT,
                       name TEXT UNIQUE,
                       description TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (innovation_proposal_id) REFERENCES innovation_proposal (id) ON DELETE CASCADE
                       )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS innovation_proposal_embeddings (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       innovation_proposal_id INTEGER,
                       name TEXT UNIQUE,
                       embedding_name BLOB NOT NULL,
                       embedding_description BLOB NOT NULL,
                       embedding_general BLOB NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (innovation_proposal_id) REFERENCES innovation_proposal (id) ON DELETE CASCADE
                       )""")
        conn.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS innovation_proposal_prompt (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       prompt TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )""")
        conn.commit()
        
#--------------------------------------------innovation_proposal--------------------------------------------

    def add_innovation_proposal(self, filename, filepath):
        conn, cursor = self._get_connection()

        try:
            cursor.execute("INSERT INTO innovation_proposal (filename, filepath) VALUES (?, ?)",
                        (filename, filepath))
            conn.commit()
        except sqlite3.IntegrityError as IntegrityError:
            return f"DATABASE ERROR - {IntegrityError}"
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
    def get_path_from_innovation_proposal(self, filename):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("SELECT filepath FROM innovation_proposal WHERE filename = (?)",
                           (filename,))
            path = cursor.fetchone()
            return path
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
    def delete_innovation_proposal(self, filename):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("DELETE FROM innovation_proposal WHERE filename = (?)",
                           (filename,))
            conn.commit()
        except Exception as e:
            return f"DATABASE ERROR - {e}"

#--------------------------------------------key_information--------------------------------------------
    
    def add_key_information(self, filename, registered, name, description):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""INSERT INTO innovation_proposal_info (innovation_proposal_id, registered, name, description)
                           SELECT id, ?, ?, ? FROM innovation_proposal
                           WHERE filename = ?
                           """, (registered, name, description, filename))
            conn.commit()
    
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
    def get_key_information(self):
        conn, cursor = self._get_connection()
        try:
            result = cursor.execute("""SELECT innovation_proposal.filename,
                                    innovation_proposal_info.registered,
                                    innovation_proposal_info.name
                                    FROM innovation_proposal
                                    LEFT JOIN innovation_proposal_info ON innovation_proposal.id = innovation_proposal_info.innovation_proposal_id
                                    """)
            data = result.fetchall()
            return data
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
    def get_name_description(self, filename):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""SELECT innovation_proposal_info.name, innovation_proposal_info.description
                                    FROM innovation_proposal
                                    LEFT JOIN innovation_proposal_info ON innovation_proposal.id = innovation_proposal_info.innovation_proposal_id
                                    WHERE innovation_proposal.filename = ?""",
                                    (filename[:-4],))
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
    def update_key_information(self, filename, new_registered, new_name):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""SELECT registered, name FROM innovation_proposal_info 
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

            cursor.execute("""UPDATE innovation_proposal_info SET registered = ?, name = ?
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

    def add_embedding(self, filename, embedding_name, embedding_description, embedding_general):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""SELECT innovation_proposal.id,
                                    innovation_proposal_info.name
                                    FROM innovation_proposal
                                    LEFT JOIN innovation_proposal_info ON innovation_proposal.id = innovation_proposal_info.innovation_proposal_id
                                    WHERE innovation_proposal.filename = ?""",
                                    (filename[:-4],))
            result = cursor.fetchone()

            embedding_name_bytes = np.array(embedding_name, dtype=np.float32).tobytes()
            embedding_description_bytes = np.array(embedding_description, dtype=np.float32).tobytes()
            embedding_general_bytes = np.array(embedding_general, dtype=np.float32).tobytes()

            cursor.execute("INSERT OR IGNORE INTO innovation_proposal_embeddings (innovation_proposal_id, name, embedding_name, embedding_description, embedding_general) VALUES (?, ?, ?, ?, ?)",
                               (result[0], result[1], embedding_name_bytes, embedding_description_bytes, embedding_general_bytes))
            conn.commit()
        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
    def get_embeddings(self, value):
        conn, cursor = self._get_connection()
        try:
            result = cursor.execute("SELECT name, embedding_name, embedding_description, embedding_general FROM innovation_proposal_embeddings")
            embedding_list = []
            for i in result.fetchall():
                name = i[0]
                embedding_name_bytes = i[1]
                embedding_description_bytes = i[2]
                embedding_general_bytes = i[3]
                embedding_name_numpy = np.frombuffer(embedding_name_bytes, dtype=np.float32)
                embedding_description_numpy = np.frombuffer(embedding_description_bytes, dtype=np.float32)
                embedding_general_numpy = np.frombuffer(embedding_general_bytes, dtype=np.float32)

                if value == "name":
                    embedding_list.append([name, embedding_name_numpy])
                elif value == "description":
                    embedding_list.append([name, embedding_description_numpy])
                elif value == "general":
                    embedding_list.append([name, embedding_general_numpy])
                    
            if embedding_list == []:
                return None
            else:
                return embedding_list

        except Exception as e:
            return f"DATABASE ERROR - {e}"
    
    def update_embedding(self, filename, embedding):
        conn, cursor = self._get_connection()
        try:
            cursor.execute("""SELECT innovation_proposal.id,
                                    innovation_proposal_info.name
                                    FROM innovation_proposal
                                    LEFT JOIN innovation_proposal_info ON innovation_proposal.id = innovation_proposal_info.innovation_proposal_id
                                    WHERE innovation_proposal.filename = ?""",
                                    (filename,))
            result = cursor.fetchone()
            print(result)
    
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            cursor.execute("""UPDATE innovation_proposal_embeddings 
                            SET innovation_proposal_id = ?, name = ?, embedding_name = ?
                            WHERE innovation_proposal_id = ?""",
                        (result[0], result[1], embedding_bytes, result[0]))
            conn.commit()

        except Exception as e:
            return f"DATABASE ERROR - {e}"

#--------------------------------------------prompt_text--------------------------------------------

    def add_prompt_text(self, prompt):
            conn, cursor = self._get_connection()

            try:
                cursor.execute("INSERT INTO innovation_proposal_prompt prompt VALUES ?",
                            (prompt,))
                conn.commit()
            except Exception as e:
                return f"DATABASE ERROR - {e}"
    
    def update_prompt_text(self, new_prompt):
            conn, cursor = self._get_connection()

            try:
                cursor.execute("UPDATE innovation_proposal_prompt SET prompt = ? WHERE id = 1",
                            (new_prompt,))
                conn.commit()
            except Exception as e:
                return f"DATABASE ERROR - {e}"
    
    def get_prompt_text(self):
            conn, cursor = self._get_connection()

            try:
                cursor.execute("SELECT prompt INTO innovation_proposal_prompt WHERE id = 1")

                prompt_text = cursor.fetchone()
                return prompt_text[0]
            except Exception as e:
                return f"DATABASE ERROR - {e}"

#--------------------------------------------DB_CLOSE--------------------------------------------

    def close(self):
        self.connection.close()
