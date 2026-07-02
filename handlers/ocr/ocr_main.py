from handlers.ocr.load_file import Load_file
from handlers.ocr.conversion import Conversion_Thread
from handlers.ocr.processing import Processing_Thread
from handlers.ocr.recognition import Recognition_Thread
from handlers.ocr.extraction import Extraction
import os

from data.data import ocr_result

class OCR_main:
    def __init__(self, db, parent = None):
        self.parent = parent
        self.db = db
        self.thread = None
    
    def start(self):
        self.load_file = Load_file(self.parent, self.db)
        signal = self.load_file.start()
        if signal == None:
            pass
        elif signal == True:
            self.conversion_thread()
    
    def conversion_thread(self):
        self.parent.gui.pushButton.setEnabled(False)
        self.parent.gui.pushButton.setText("КОНВЕРТАЦИЯ...")
        filename = self.parent.gui.label_4.text()
        self.thread = Conversion_Thread(filename, self.db)
        self.thread.conversion_finished.connect(self.conversion_finished)
        self.thread.conversion_error.connect(self.conversion_error)
        self.thread.start()
    
    def conversion_finished(self):
        self.parent.gui.pushButton.setText("ОБРАБОТКА...")
        self.thread.deleteLater()
        self.processing_thread()
    
    def conversion_error(self, error):
        print(f"errorconv - {error}")
        self.thread.deleteLater()

    def processing_thread(self):
        self.thread = Processing_Thread()
        self.thread.processing_finished.connect(self.processing_finished)
        self.thread.processing_error.connect(self.processing_error)
        self.thread.start()

    def processing_finished(self):
        self.parent.gui.pushButton.setText("РАСПОЗНОВАНИЕ...")
        self.thread.deleteLater()
        self.recognition_thread()

    def processing_error(self, error):
        print(f"errorproccess - {error}")
        self.thread.deleteLater()

    def recognition_thread(self):
        self.thread = Recognition_Thread()
        self.thread.recognition_finished.connect(self.recognition_finished)
        self.thread.recognition_error.connect(self.recognition_error)
        self.thread.start()
    
    def recognition_finished(self, result):
        self.parent.gui.pushButton.setEnabled(True)
        self.parent.gui.pushButton.setText("Загрузить документ")
        
        registered = result[0]
        name = result[1]
        author = result[2]

        self.extraction = Extraction()
        number, date = self.extraction.extrection(registered)
        
        filename = self.parent.gui.label_4.text()
        self.db.add_key_information(filename[:-4], number, date, name, author)
        text = ocr_result(number, date, name, author)
        self.parent.gui.plainTextEdit.setPlainText(text)
        self.thread.deleteLater()
        self.clear_folder()
    
    def recognition_error(self, error):
        print(f"errorrecogni - {error}")
        self.thread.deleteLater()
        self.clear_folder()

    def clear_folder(self):
        pass

if __name__ == "__main__":
    OCR_main()