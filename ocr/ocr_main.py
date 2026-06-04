from ocr.conversion import Conversion_Thread
from ocr.processing import Processing_Thread
from ocr.recognition import Recognition_Thread

class OCR_main:
    def __init__(self, parent = None):
        self.parent = parent
        self.ocr_result = None
        self.thread = None
        self.start_ocr()
    
    def start_ocr(self):
        self.conversion_thread()
    
    def conversion_thread(self):
        # self.parent.pushButton2.setEnabled(False)
        # self.parent.pushButton2.setText("КОНВЕРТАЦИЯ...")
        self.thread = Conversion_Thread()
        self.thread.conversion_finished.connect(self.conversion_finished)
        self.thread.conversion_error.connect(self.conversion_error)
        self.thread.start()
    
    def conversion_finished(self):
        self.thread.deleteLater()
        self.processing_thread()
    
    def conversion_error(self, error):
        print(f"error - {error}")
        self.thread.deleteLater()

    def processing_thread(self):
        # self.parent.pushButton2.setText("ОБРАБОТКА...")
        self.thread = Processing_Thread()
        self.thread.processing_finished.connect(self.processing_finished)
        self.thread.processing_error.connect(self.processing_error)
        self.thread.start()

    def processing_finished(self):
        self.thread.deleteLater()
        self.recognition_thread()

    def processing_error(self, error):
        print(f"error - {error}")
        self.thread.deleteLater()

    def recognition_thread(self):
        # self.parent.pushButton2.setEnabled(True)
        # self.parent.pushButton2.setText("РАСПОЗНОВАНИЕ...")
        self.thread = Recognition_Thread()
        self.thread.recognition_finished.connect(self.recognition_finished)
        self.thread.recognition_error.connect(self.recognition_error)
        self.thread.start()
    
    def recognition_finished(self, result):
        self.ocr_result = result
        self.thread.deleteLater()

    
    def recognition_error(self, error):
        print(f"error - {error}")
        self.thread.deleteLater()

if __name__ == "__main__":
    OCR_main()