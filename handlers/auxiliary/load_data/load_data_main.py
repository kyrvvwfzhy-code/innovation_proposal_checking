from PyQt5.QtWidgets import QFileDialog, QMessageBox
from handlers.auxiliary.load_data.load_files import Load_files
from handlers.auxiliary.load_data.conversion_data import Conversion_data_Thread
from handlers.auxiliary.load_data.processing_data import Processing_data_Thread
from handlers.auxiliary.load_data.recognition_data import Recognition_data_Thread
from handlers.auxiliary.load_data.embedding_data import Embedding_data_Thread
from handlers.options.progressbar.progressbar_thread import Progressbar_Thread
from data.messagebox import critical_message
import os

from log.logging import logger

class Load_data_main:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None

    def start(self):
        self.load_files = Load_files(self.db)
        self.filename_list = self.load_files.start()
        if self.filename_list != None:
            self.target = (len(self.filename_list) * 3)
            self.start_progressbar()
            self.conversion_data_thread(self.filename_list)
        else:
            critical_message(self.parent, "Выберите папку с файлами")
            pass
    
    def start_progressbar(self):
        self.parent.show()
        self.progressbar = Progressbar_Thread(self.parent, self.target)
        self.progressbar.progress_update.connect(lambda : self.progressbar.deleteLater)
        self.progressbar.start()
    
    def conversion_data_thread(self, filename_list):
        logger.info("START (load_data) - Conversion")
        self.thread = Conversion_data_Thread(self.db, filename_list)
        self.thread.conversion_data_finished.connect(self.conversion_data_finished)
        self.thread.conversion_data_error.connect(self.conversion_data_error)
        self.thread.start()

    def conversion_data_finished(self):
        logger.info(f"CONVERSION (load_data) - is Ready")
        self.thread.deleteLater()
        self.processing_data_thread()
    
    def conversion_data_error(self, error):
        logger.error(f"CONVERSION (load_data) - {error}")
        self.thread.deleteLater()
    
    def processing_data_thread(self):
        logger.info(f"START (load_data) - Processing")
        self.thread = Processing_data_Thread()
        self.thread.processing_data_finished.connect(self.processing_data_finished)
        self.thread.processing_data_error.connect(self.processing_data_error)
        self.thread.start()
    
    def processing_data_finished(self):
        logger.info(f"PROCESSING (load_data) - is Ready")
        self.thread.deleteLater()
        self.recognition_data_thread()

    def processing_data_error(self, error):
        logger.error(f"PROCESSING (load_data) - {error}")
        self.thread.deleteLater()

    def recognition_data_thread(self):
        logger.info(f"START (load_data) - Recognition")
        self.thread = Recognition_data_Thread(self.db, self.filename_list)
        self.thread.recognition_data_finished.connect(self.recognition_data_finished)
        self.thread.recognition_data_error.connect(self.recognition_data_error)
        self.thread.start()
    
    def recognition_data_finished(self, result):
        logger.info(f"RECOGNTION (load_data) - is Ready")
        self.thread.deleteLater()
        self.embedding_data_thread(result)
    
    def recognition_data_error(self, error):
        logger.error(f"RECOGNITION (load_data) - {error}")
        self.thread.deleteLater()
    
    def embedding_data_thread(self, result):
        logger.info(f"START (load_data) - EMBEDDING")
        self.thread = Embedding_data_Thread(self.db, self.filename_list, result[0], result[1])
        self.thread.embedding_data_finished.connect(self.embedding_data_finished)
        self.thread.embedding_data_error.connect(self.embedding_data_error)
        self.thread.start()

    def embedding_data_finished(self, text):
        logger.info(f"EMBEDDING (load_data) - is Ready")
        self.clear_folder()
        self.thread.deleteLater()

    def embedding_data_error(self, error):
        logger.error(f"EMBEDDING (load_data) - {error}")
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
        logger.info(f"'OCR_TMP' folder from (load_data) is clear")




