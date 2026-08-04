from handlers.engine.ocr.load_file import Load_file
from handlers.engine.ocr.conversion import Conversion_Thread
from handlers.engine.ocr.processing import Processing_Thread
from handlers.engine.ocr.recognition import Recognition_Thread
import os

from data.messagebox import critical_message
from handlers.options.progressbar.progressbar_thread import Progressbar_Thread
from handlers.engine.ocr.embedding import Embedding_Thread

from data.data import ocr_result
from log.logging import logger

class OCR_main:
    def __init__(self, db, level, parent = None, callback = None):
        self.parent = parent
        self.db = db
        self.level = level
        self.thread = None
        self.callback = callback
    
    def start(self):
        if self.level == "download":
            logger.debug(f"OCR используется на уровне - {self.level}")
            self.load_file = Load_file(db = self.db, level = self.level, parent = self.parent)
            signal = self.load_file.start()
            if signal == None:
                pass
            elif signal == True:
                self.conversion_thread()

        elif self.level == "settings":
            self.load_files = Load_file(db = self.db, level = self.level)
            self.filename_list = self.load_files.start()
            if self.filename_list != None:
                self.target = (len(self.filename_list) * 3)
                self.start_progressbar()
                self.conversion_thread(filename_list = self.filename_list)
            else:
                critical_message(self.parent, "Выберите папку с файлами")
                pass

    def start_progressbar(self):
        self.parent.show()
        self.progressbar = Progressbar_Thread(self.parent, self.target)
        self.progressbar.progress_update.connect(lambda : self.progressbar.deleteLater)
        self.progressbar.start()
    
    def conversion_thread(self, filename_list = None):
        if self.level == "download":
            logger.info("START - Conversion")
            self.parent.gui.pushButton.setEnabled(False)
            self.parent.gui.pushButton.setText("КОНВЕРТАЦИЯ...")
            filename = self.parent.gui.label_4.text()
            self.thread = Conversion_Thread(db = self.db, level = self.level, level_data = filename)
            self.thread.conversion_finished.connect(self.conversion_finished)
            self.thread.conversion_error.connect(self.conversion_error)
            self.thread.start()
        elif self.level == "settings":
            logger.info("START (load_data) - Conversion")
            self.thread = Conversion_Thread(db = self.db, level = self.level, level_data = filename_list)
            self.thread.conversion_finished.connect(self.conversion_finished)
            self.thread.conversion_error.connect(self.conversion_error)
            self.thread.start()
    
    def conversion_finished(self):
        if self.level == "download":
            logger.info(f"CONVERSION - is Ready")
            self.parent.gui.pushButton.setText("ОБРАБОТКА...")
            self.thread.deleteLater()
            self.processing_thread()
        elif self.level == "settings":
            logger.info(f"CONVERSION (load_data) - is Ready")
            self.thread.deleteLater()
            self.processing_thread()
    
    def conversion_error(self, error):
        if self.level == "download":
            logger.error(f"CONVERSION - {error}")
            self.thread.deleteLater()
        elif self.level == "settings":
            logger.error(f"CONVERSION (load_data) - {error}")
            self.thread.deleteLater()

    def processing_thread(self):
        if self.level == "download":
            logger.info(f"START - Processing")
            self.thread = Processing_Thread(level = self.level)
            self.thread.processing_finished.connect(self.processing_finished)
            self.thread.processing_error.connect(self.processing_error)
            self.thread.start()
        elif self.level == "settings":
            logger.info(f"START (load_data) - Processing")
            self.thread = Processing_Thread(level = self.level)
            self.thread.processing_finished.connect(self.processing_finished)
            self.thread.processing_error.connect(self.processing_error)
            self.thread.start()

    def processing_finished(self):
        if self.level == "download":
            logger.info(f"PROCESSING - is Ready")
            self.parent.gui.pushButton.setText("РАСПОЗНОВАНИЕ...")
            self.thread.deleteLater()
            self.recognition_thread()
        elif self.level == "settings":
            logger.info(f"PROCESSING (load_data) - is Ready")
            self.thread.deleteLater()
            self.recognition_thread()

    def processing_error(self, error):
        if self.level == "download":
            logger.error(f"PROCESSING - {error}")
            self.thread.deleteLater()
        elif self.level == "settings":
            logger.error(f"PROCESSING (load_data) - {error}")
            self.thread.deleteLater()

    def recognition_thread(self):
        if self.level == "download":
            logger.info(f"START - Recognition")
            self.thread = Recognition_Thread(level = self.level)
            self.thread.recognition_finished.connect(self.recognition_finished)
            self.thread.recognition_error.connect(self.recognition_error)
            self.thread.start()
        elif self.level == "settings":
            logger.info(f"START (load_data) - Recognition")
            self.thread = Recognition_Thread(db = self.db, level = self.level, filename_list = self.filename_list)
            self.thread.recognition_finished.connect(self.recognition_finished)
            self.thread.recognition_error.connect(self.recognition_error)
            self.thread.start()
    
    def recognition_finished(self, result):
        if self.level == "download":
            logger.info(f"RECOGNTION - is Ready")
            self.parent.gui.pushButton.setEnabled(True)
            self.parent.gui.pushButton.setText("Загрузить документ")
            
            self.filename = self.parent.gui.label_4.text()
            self.registered = result[0]
            self.name = result[1]
            self.description = result[2]

            text = ocr_result(self.registered, self.name, self.description)
            self.parent.gui.plainTextEdit.setPlainText(text)

            self.thread.deleteLater()
            self.clear_folder()

            if self.callback:
                self.callback(self.filename, self.registered, self.name, self.description)
        elif self.level == "settings":
            logger.info(f"RECOGNTION (load_data) - is Ready")
            self.thread.deleteLater()
            self.embedding_data_thread(result)

    def recognition_error(self, error):
        if self.level == "download":
            logger.error(f"RECOGNITION - {error}")
            self.thread.deleteLater()
            self.clear_folder()
        elif self.level == "settings":
            logger.error(f"RECOGNITION (load_data) - {error}")
            self.thread.deleteLater()

    def embedding_data_thread(self, result):
            logger.info(f"START (load_data) - EMBEDDING")
            self.thread = Embedding_Thread(self.db, self.filename_list, result[0], result[1])
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
        logger.info(f"'OCR_TMP' folder is clear")

if __name__ == "__main__":
    OCR_main()