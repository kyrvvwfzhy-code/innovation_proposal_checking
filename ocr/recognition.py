from PyQt5.QtCore import QThread, pyqtSignal
import pytesseract

class Recognition_Thread(QThread):
    recognition_finished = pyqtSignal(str)
    recognition_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            result = self.recognition()
            self.recognition_finished.emit(result)
        except Exception as e:
            self.recognition_error.emit(f"Error - {e}")

    def recognition(self):
        path = "OCR_TMP/page_1_processed.png"
        text = pytesseract.image_to_string(path, lang='rus+eng')
        return text
    
if __name__ == "__main__":
    start = Recognition_Thread()
    start.recognition_finished.connect(lambda dg: print(f"recognition_finished {dg}"))
    start.recognition_error.connect(lambda dw: print(f"recognition_error {dw}"))
    start.run()