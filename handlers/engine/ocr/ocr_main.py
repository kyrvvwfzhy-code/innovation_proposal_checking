from handlers.engine.ocr.load_file import Load_file
from handlers.engine.ocr.conversion import Conversion_Thread
from handlers.engine.ocr.processing import Processing_Thread
from handlers.engine.ocr.recognition import Recognition_Thread
from handlers.engine.ocr.embedding import Embedding_Thread

from handlers.options.progressbar.progressbar_thread import Progressbar_Thread

from data.messagebox import critical_message
from data.data import ocr_result

from log.logging import logger
import os


class OCR:
    def __init__(self, db, level, parent = None, callback = None):
        self.parent = parent
        self.db = db
        self.level = level
        self.thread = None
        self.callback = callback
    
    def start(self):
        logger.info(f"OCR | STARTING... - {self.level} level")
        if self.level == "download":
            self.load_file = Load_file(db = self.db, level = self.level, parent = self.parent)
            filename = self.load_file.start()
            logger.info(f"OCR | FILE - \"{filename}\" selected")
            if filename:
                self.conversion_thread()
            elif filename == None:
                pass

        elif self.level == "settings":
            self.load_files = Load_file(db = self.db, level = self.level)
            self.filename_list = self.load_files.start()
            if self.filename_list == None:
                logger.info("OCR | FOLDER - not selected")
                critical_message(self.parent, "Выберите папку с файлами")
                pass
            elif len(self.filename_list) == 0:
                logger.info("OCR | FILE - is loaded yet")
                critical_message(self.parent, "Выбранные документы уже выгружены")
                pass

            elif self.filename_list != None:
                self.target = (len(self.filename_list))
                self.start_progressbar()
                self.conversion_thread(filename_list = self.filename_list)

    def start_progressbar(self):
        self.parent.show()
        self.progressbar = Progressbar_Thread(self.parent, self.db, self.target)
        self.progressbar.progress_update.connect(lambda : self.progressbar.deleteLater)
        self.progressbar.start()
    
    def conversion_thread(self, filename_list = None):
        logger.info("OCR | START - Conversion")

        if self.level == "download":
            self.parent.gui.pushButton.setEnabled(False)
            self.parent.gui.pushButton.setText("КОНВЕРТАЦИЯ...")
            filename = self.parent.gui.label_4.text()
            self.thread = Conversion_Thread(db = self.db, level = self.level, level_data = filename)
            self.thread.conversion_finished.connect(self.conversion_finished)
            self.thread.conversion_error.connect(self.conversion_error)
            self.thread.start()
        elif self.level == "settings":
            self.thread = Conversion_Thread(db = self.db, level = self.level, level_data = filename_list)
            self.thread.conversion_finished.connect(self.conversion_finished)
            self.thread.conversion_error.connect(self.conversion_error)
            self.thread.start()
    
    def conversion_finished(self):
        logger.info("OCR | FINISHED - Convesion")

        if self.level == "download":
            self.parent.gui.pushButton.setText("ОБРАБОТКА...")
            self.thread.deleteLater()
            self.processing_thread()
        elif self.level == "settings":
            self.thread.deleteLater()
            self.processing_thread()
    
    def conversion_error(self, error):
        logger.error(f"OCR | FINISHED - Conversion : {error}")

        if self.level == "download":
            self.thread.deleteLater()
        elif self.level == "settings":
            self.thread.deleteLater()

    def processing_thread(self):
        logger.info("OCR | START - Processing")

        if self.level == "download":
            self.thread = Processing_Thread(level = self.level)
            self.thread.processing_finished.connect(self.processing_finished)
            self.thread.processing_error.connect(self.processing_error)
            self.thread.start()
        elif self.level == "settings":
            self.thread = Processing_Thread(level = self.level)
            self.thread.processing_finished.connect(self.processing_finished)
            self.thread.processing_error.connect(self.processing_error)
            self.thread.start()

    def processing_finished(self):
        logger.info("OCR | FINISHED - Processing")

        if self.level == "download":
            self.parent.gui.pushButton.setText("РАСПОЗНОВАНИЕ...")
            self.thread.deleteLater()
            self.recognition_thread()
        elif self.level == "settings":
            self.thread.deleteLater()
            self.recognition_thread()

    def processing_error(self, error):
        logger.error(f"OCR | FINISHED - Processing : {error}")
        if self.level == "download":
            self.thread.deleteLater()
        elif self.level == "settings":
            self.thread.deleteLater()

    def recognition_thread(self):
        logger.info("OCR | START - Recognition")

        if self.level == "download":
            self.thread = Recognition_Thread(level = self.level)
            self.thread.recognition_finished.connect(self.recognition_finished)
            self.thread.recognition_error.connect(self.recognition_error)
            self.thread.start()
        elif self.level == "settings":
            self.thread = Recognition_Thread(db = self.db, level = self.level, filename_list = self.filename_list)
            self.thread.recognition_finished.connect(self.recognition_finished)
            self.thread.recognition_error.connect(self.recognition_error)
            self.thread.start()
    
    def recognition_finished(self, result):
        logger.info("OCR | FINISHED - Recognition")

        if self.level == "download":
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
            self.thread.deleteLater()
            self.embedding_data_thread(result)

    def recognition_error(self, error):
        logger.error(f"OCR | FINISHED - Recognition : {error}")

        if self.level == "download":
            self.thread.deleteLater()
            self.clear_folder()
        elif self.level == "settings":
            self.thread.deleteLater()

    def embedding_data_thread(self, result):
            logger.info("OCR | START - Embedding")
            self.thread = Embedding_Thread(self.db, self.filename_list, result[0], result[1])
            self.thread.embedding_data_finished.connect(self.embedding_data_finished)
            self.thread.embedding_data_error.connect(self.embedding_data_error)
            self.thread.start()

    def embedding_data_finished(self):
        logger.info("OCR | FINISHED - Embedding")
        self.clear_folder()
        self.thread.deleteLater()

    def embedding_data_error(self, error):
        logger.error(f"OCR | FINISHED - Embedding : {error}")
        self.thread.deleteLater()

    def clear_folder(self):
        logger.info("OCR | CLEAN - tmp folder")
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            paths = []
            for filename in os.listdir(folder_path):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    paths.append(full_path)
                    os.remove(full_path)