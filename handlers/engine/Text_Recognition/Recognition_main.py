from handlers.engine.Text_Recognition.load_file import Load_file
from handlers.engine.Text_Recognition.conversion import Conversion_Thread
from handlers.engine.Text_Recognition.processing import Processing_Thread
from handlers.engine.Text_Recognition.forming import Forming_Thread
from handlers.engine.Text_Recognition.vectorization import Vectorization_Thread

from data.messagebox import critical_message
from data.output_message import text_recognition_output

from log.logging import logger
import os

class Text_Recognition_main:
    def __init__(self, db, level, model, parent = None, callback = None):
        self.parent = parent
        self.db = db
        self.level = level
        self.callback = callback
        self.model = model
        self.thread = None
    
    def start(self):
        logger.info(f"TEXT RECOGNITION | STARTING... - {self.level} level")
        self.clear_folder()
        
        if self.level == "download":
            self.load_file = Load_file(db = self.db, level = self.level, parent = self.parent)
            filename = self.load_file.start()
            if filename:
                logger.info(f"TEXT RECOGNITION | SELECT - \"{filename}\" is select")
                self.conversion_thread()
            elif filename == False:
                critical_message(self.parent, f"Данный документ уже выгружен")
                self.parent.gui.label_4.clear()
            else:
                pass

        elif self.level == "settings":
            self.load_files = Load_file(db = self.db, level = self.level)
            self.filename_list = self.load_files.start()
            if self.filename_list == None:
                logger.info("TEXT RECOGNITION | SELECT - path not selected")
                critical_message(self.parent, "Выберите папку с файлами")
                pass
            elif len(self.filename_list) == 0:
                logger.info("TEXT RECOGNITION | SELECT - file is loaded yet")
                critical_message(self.parent, "Выбранные документы уже выгружены")
                pass

            elif self.filename_list != None:
                self.target = (len(self.filename_list))
                self.conversion_thread(filename_list = self.filename_list)
    
    def conversion_thread(self, filename_list = None):
        logger.info("TEXT RECOGNITION | START - Conversion")

        if self.level == "download":
            self.parent.gui.pushButton.setEnabled(False)
            self.parent.gui.pushButton.setText("КОНВЕРТАЦИЯ...")
            filename = self.parent.gui.label_4.text()
            self.thread = Conversion_Thread(db = self.db, level = self.level, level_data = filename)
        
        elif self.level == "settings":
            self.parent.progressbar.open(self.target)
            self.thread = Conversion_Thread(db = self.db, level = self.level, level_data = filename_list)

        self.thread.conversion_finished.connect(self.conversion_finished)
        self.thread.conversion_error.connect(self.conversion_error)
        self.thread.start()

    def conversion_finished(self):
        logger.info("TEXT RECOGNITION | FINISHED - Conversion (SUCCESS)")
        self.thread.deleteLater()

        if self.level == "download":
            self.parent.gui.pushButton.setText("ОБРАБОТКА...")

        self.processing_thread()
    
    def conversion_error(self, error):
        logger.error(f"TEXT RECOGNITION | FINISHED - Conversion (ERROR): {error}")
        self.thread.deleteLater()

    def processing_thread(self):
        logger.info("TEXT RECOGNITION | START - Processing")

        if self.level == "download":
            self.thread = Processing_Thread(level = self.level)
     
        elif self.level == "settings":
            self.thread = Processing_Thread(level = self.level)

        self.thread.processing_finished.connect(self.processing_finished)
        self.thread.processing_error.connect(self.processing_error)
        self.thread.start()

    def processing_finished(self):
        logger.info("TEXT RECOGNITION | FINISHED - Processing (SUCCESS)")
        self.thread.deleteLater()

        if self.level == "download":
            self.parent.gui.pushButton.setText("РАСПОЗНОВАНИЕ...")

        self.recognition_thread()

    def processing_error(self, error):
        logger.error(f"TEXT RECOGNITION | FINISHED - Processing (ERROR): {error}")
        self.thread.deleteLater()

    def recognition_thread(self):
        logger.info("TEXT RECOGNITION | START - Recognition")

        if self.level == "download":
            self.thread = Forming_Thread(level = self.level)

        elif self.level == "settings":
            self.thread = Forming_Thread(db = self.db, level = self.level, filename_list = self.filename_list)

        self.thread.recognition_finished.connect(self.recognition_finished)
        self.thread.recognition_error.connect(self.recognition_error)
        self.thread.start()
    
    def recognition_finished(self, result):
        logger.info("TEXT RECOGNITION | FINISHED - Recognition (SUCCESS)")
        self.thread.deleteLater()

        if self.level == "download":
            self.parent.gui.pushButton.setText("Загрузить документ")
            
            self.filename = self.parent.gui.label_4.text()
            self.registered = result[0]
            self.name = result[1]
            self.description = result[2]

            text = text_recognition_output(self.registered, self.name, self.description)
            self.parent.gui.plainTextEdit.setPlainText(text)

            if self.callback:
                self.callback(self.filename, self.registered, self.name, self.description)
            logger.info("TEXT RECOGNITION | SUCCESSFULL FINISHED")
                
        elif self.level == "settings":
            self.vectorization_data_thread(result)

    def recognition_error(self, error):
        logger.error(f"TEXT RECOGNITION | FINISHED - Recognition (ERROR): {error}")
        self.thread.deleteLater()

    def vectorization_data_thread(self, result):
            logger.info("TEXT RECOGNITION | START - vectorization")
            self.thread = Vectorization_Thread(self.db, self.filename_list, result[0], result[1], self.model)
            self.thread.vectorization_data_finished.connect(self.vectorization_data_finished)
            self.thread.vectorization_data_error.connect(self.vectorization_data_error)
            self.thread.start()

    def vectorization_data_finished(self):
        logger.info("TEXT RECOGNITION | FINISHED - vectorization (SUCCESS)")
        self.thread.deleteLater()
        logger.info("DATA LOAD | SUCCESSFULL FINISHED)")

    def vectorization_data_error(self, error):
        logger.error(f"TEXT RECOGNITION | FINISHED - vectorization (ERROR): {error}")
        self.thread.deleteLater()

    def clear_folder(self):
        logger.info("TEXT RECOGNITION | CLEAN - tmp folder")
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            paths = []
            for filename in os.listdir(folder_path):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    paths.append(full_path)
                    os.remove(full_path)