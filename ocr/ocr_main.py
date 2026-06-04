from ocr.conversion import Conversion_Thread
from ocr.processing import Processing_Thread
from ocr.recognition import Recognition_Thread
import os

class OCR_main:
    def __init__(self, parent = None):
        self.parent = parent
        self.ocr_result = None
        self.thread = None
    
    def start_ocr(self):
        self.conversion_thread()
    
    def conversion_thread(self):
        self.parent.gui.pushButton_2.setEnabled(False)
        self.parent.gui.pushButton_2.setText("КОНВЕРТАЦИЯ...")
        self.thread = Conversion_Thread()
        self.thread.conversion_finished.connect(self.conversion_finished)
        self.thread.conversion_error.connect(self.conversion_error)
        self.thread.start()
    
    def conversion_finished(self):
        self.parent.gui.pushButton_2.setText("ОБРАБОТКА...")
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
        self.parent.gui.pushButton_2.setText("РАСПОЗНОВАНИЕ...")
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
        self.parent.gui.pushButton_2.setEnabled(True)
        self.parent.gui.pushButton_2.setText("Начать проверку")
        self.parent.gui.plainTextEdit.setPlainText(result)
        self.thread.deleteLater()
        self.clear_folder()
    
    def recognition_error(self, error):
        print(f"errorrecogni - {error}")
        self.thread.deleteLater()
        self.clear_folder()

    def clear_folder(self):
        pass
        # folder_path = "OCR_TMP"
        # if os.path.exists(folder_path):
        #     paths = []
        #     for filename in os.listdir(folder_path):
        #         full_path = os.path.join(folder_path, filename)
        #         if os.path.isfile(full_path):
        #             paths.append(full_path)
        #             os.remove(full_path)

if __name__ == "__main__":
    OCR_main()