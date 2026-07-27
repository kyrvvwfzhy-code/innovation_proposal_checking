from handlers.engine.ocr.load_file import Load_file
from handlers.engine.ocr.conversion import Conversion_Thread
from handlers.engine.ocr.processing import Processing_Thread
from handlers.engine.ocr.recognition import Recognition_Thread
import os

from data.data import ocr_result
from log.logging import logger

class OCR_main:
    def __init__(self, db, parent = None, callback = None):
        self.parent = parent
        self.db = db
        self.thread = None
        self.callback = callback
    
    def start(self):
        self.parent.gui.pushButton_2.setEnabled(False)
        self.load_file = Load_file(self.parent, self.db)
        signal = self.load_file.start()
        if signal == None:
            pass
        elif signal == True:
            self.conversion_thread()
    
    def conversion_thread(self):
        logger.info("START - Conversion")
        self.parent.gui.pushButton.setEnabled(False)
        self.parent.gui.pushButton.setText("КОНВЕРТАЦИЯ...")
        filename = self.parent.gui.label_4.text()
        self.thread = Conversion_Thread(filename, self.db)
        self.thread.conversion_finished.connect(self.conversion_finished)
        self.thread.conversion_error.connect(self.conversion_error)
        self.thread.start()
    
    def conversion_finished(self):
        logger.info(f"CONVERSION - is Ready")
        self.parent.gui.pushButton.setText("ОБРАБОТКА...")
        self.thread.deleteLater()
        self.processing_thread()
    
    def conversion_error(self, error):
        logger.error(f"CONVERSION - {error}")
        self.thread.deleteLater()

    def processing_thread(self):
        logger.info(f"START - Processing")
        self.thread = Processing_Thread()
        self.thread.processing_finished.connect(self.processing_finished)
        self.thread.processing_error.connect(self.processing_error)
        self.thread.start()

    def processing_finished(self):
        logger.info(f"PROCESSING - is Ready")
        self.parent.gui.pushButton.setText("РАСПОЗНОВАНИЕ...")
        self.thread.deleteLater()
        self.recognition_thread()

    def processing_error(self, error):
        logger.error(f"PROCESSING - {error}")
        self.thread.deleteLater()

    def recognition_thread(self):
        logger.info(f"START - Recognition")
        self.thread = Recognition_Thread()
        self.thread.recognition_finished.connect(self.recognition_finished)
        self.thread.recognition_error.connect(self.recognition_error)
        self.thread.start()
    
    def recognition_finished(self, result):
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
    
    def recognition_error(self, error):
        logger.error(f"RECOGNITION - {error}")
        self.thread.deleteLater()
        self.clear_folder()

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