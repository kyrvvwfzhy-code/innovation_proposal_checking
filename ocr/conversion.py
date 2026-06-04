
from PyQt5.QtCore import QThread, pyqtSignal
from pdf2image import convert_from_path
import os
from db.database import DataBase

class Conversion_Thread(QThread):
    conversion_finished = pyqtSignal(str)
    conversion_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.db = DataBase()

    def run(self):
        try:
            result = self.conversion()
            self.conversion_finished.emit(result)
        except Exception as e:
            self.conversion_error.emit(f"Error - {e}")

    def conversion(self):
        self.db = DataBase()
        pdf_path = self.db.get_loaded_rp()
        images = convert_from_path(pdf_path[1])

        os.makedirs("OCR_TMP", exist_ok = True)
        for i, image in enumerate(images):
            output_path = os.path.join("OCR_TMP", f"page_{pdf_path[0]}_{i+1}.png")
            image.save(output_path, "PNG")
        
        result = "Конвертация завершена."
        return result

if __name__ == "__main__":
    start = Conversion_Thread()
    start.conversion_finished.connect(lambda ad: print(f"conversion_finished {ad}"))
    start.conversion_error.connect(lambda dd: print(f"Сигнал conversion_error {dd}"))

    start.run()
