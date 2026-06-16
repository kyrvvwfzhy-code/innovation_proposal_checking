from PyQt5.QtCore import QThread, pyqtSignal
import pytesseract
import os

class Recognition_Thread(QThread):
    recognition_finished = pyqtSignal(list)
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
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            paths = []
            for filename in os.listdir(folder_path):
                if filename.endswith('_processed.png'):
                    full_path = os.path.join(folder_path, filename)
                    if os.path.isfile(full_path):
                        paths.append(full_path)
        file = sorted(paths)

        if len(file) >= 3:
            registered = pytesseract.image_to_string(file[0], lang='rus+eng')
            name = pytesseract.image_to_string(file[1], lang='rus+eng')
            author = pytesseract.image_to_string(file[2], lang='rus+eng')

        text =  [registered, name, author]

        result = [self.clean_text(item) for item in text]
        
        return result
    
    def clean_text(self, text):
        return ' '.join(str(text).replace('\n', ' ').replace('\x0c', ' ').split()).strip()
    
if __name__ == "__main__":
    start = Recognition_Thread()
    start.recognition_finished.connect(lambda dg: print(f"recognition_finished {dg}"))
    start.recognition_error.connect(lambda dw: print(f"recognition_error {dw}"))
    start.run()