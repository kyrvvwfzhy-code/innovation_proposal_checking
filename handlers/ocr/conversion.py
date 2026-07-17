
from PyQt5.QtCore import QThread, pyqtSignal
from pdf2image import convert_from_path
import os

class Conversion_Thread(QThread):
    conversion_finished = pyqtSignal(str)
    conversion_error = pyqtSignal(str)

    def __init__(self, filename, db):
        super().__init__()
        self.filename = filename[:-4]
        self.db = db

    def run(self):
        try:
            result = self.conversion()
            self.conversion_finished.emit(result)
        except Exception as e:
            self.conversion_error.emit(f"Error - {e}")

    def conversion(self):
        pdf_path = self.db.get_loaded_ip(self.filename)
        images = convert_from_path(pdf_path[0])

        first_page = 1
        # total_images = len(images)
        # last_page = min(9, total_images)

        os.makedirs("OCR_TMP", exist_ok = True)
        for i, image in enumerate(images):
            page_number = i+1
            if page_number == first_page:
                output_path = os.path.join("OCR_TMP", f"1_first_page_{self.filename}.png")
                image.save(output_path, "PNG")
            # if page_number == last_page:
            #     output_path = os.path.join("OCR_TMP", f"2_last_page_{self.filename}.png")
            #     image.save(output_path, "PNG")

if __name__ == "__main__":
    start = Conversion_Thread()
    start.conversion_finished.connect(lambda ad: print(f"conversion_finished {ad}"))
    start.conversion_error.connect(lambda dd: print(f"Сигнал conversion_error {dd}"))

    start.run()
