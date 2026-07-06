from handlers.settings.load_data.load_files import Load_files
from handlers.settings.load_data.conversion_data import Conversion_data_Thread
from handlers.settings.load_data.processing_data import Processing_data_Thread
from handlers.settings.load_data.recognition_data import Recognition_data_Thread
from handlers.settings.load_data.embedding_data import Embedding_data_Thread
import os

class Load_data_main:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None
        self.start()

    def start(self):
        self.load_files = Load_files(self.db)
        self.filename_list = self.load_files.start()
        self.conversion_data_thread(self.filename_list)

    def conversion_data_thread(self, filename_list):
        self.thread = Conversion_data_Thread(self.db, filename_list)
        self.thread.conversion_data_finished.connect(self.conversion_data_finished)
        self.thread.conversion_data_error.connect(self.conversion_data_error)
        self.thread.start()

    def conversion_data_finished(self):
        print("Conversion is end")
        self.thread.deleteLater()
        self.processing_data_thread()
    
    def conversion_data_error(self, error):
        print(f"errorconv - {error}")
        self.thread.deleteLater()
    
    def processing_data_thread(self):
        self.thread = Processing_data_Thread()
        self.thread.processing_data_finished.connect(self.processing_data_finished)
        self.thread.processing_data_error.connect(self.processing_data_error)
        self.thread.start()
    
    def processing_data_finished(self):
        print("Proccessing is end")
        self.thread.deleteLater()
        self.recognition_data_thread()

    def processing_data_error(self, error):
        print(f"errorproc - {error}")
        self.thread.deleteLater()

    def recognition_data_thread(self):
        self.thread = Recognition_data_Thread(self.db, self.filename_list)
        self.thread.recognition_data_finished.connect(self.recognition_data_finished)
        self.thread.recognition_data_error.connect(self.recognition_data_error)
        self.thread.start()
    
    def recognition_data_finished(self, names):
        print("Recognition is end")
        self.thread.deleteLater()
        self.embedding_data_thread(names)
    
    def recognition_data_error(self, error):
        print(f"errorrec- {error}")
        self.thread.deleteLater()
    
    def embedding_data_thread(self, names):
        self.thread = Embedding_data_Thread(self.db, self.filename_list, names)
        self.thread.embedding_data_finished.connect(self.embedding_data_finished)
        self.thread.embedding_data_error.connect(self.embedding_data_error)
        self.thread.start()

    def embedding_data_finished(self, text):
        print(f"Embedding is end\n\n{text}")
        self.thread.deleteLater()

    def embedding_data_error(self, error):
        print(f"erroremb- {error}")
        self.thread.deleteLater()

    def clear_folder(self):
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            paths = []
            for filename in os.listdir(folder_path):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    paths.append(full_path)
                    os.remove(full_path)




