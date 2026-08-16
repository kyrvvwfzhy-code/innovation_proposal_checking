from PyQt5.QtCore import QThread, pyqtSignal

from pdf2image import convert_from_path

import os

class Conversion_Thread(QThread):
    conversion_finished = pyqtSignal(str)
    conversion_error = pyqtSignal(str)

    def __init__(self, db, level, level_data):
        super().__init__()
        self.db = db
        self.level = level
        self.level_data = level_data

    def run(self):
        if self.level == "download":
            try:
                result = self.conversion()
                self.conversion_finished.emit(result)
            except Exception as e:
                self.conversion_error.emit(f"Error - {e}")
        elif self.level == "settings":
            try:
                os.makedirs("OCR_TMP", exist_ok = True)

                for files in self.level_data:
                    pdf_path = self.db.get_filepath_from_innovation_proposal(files[:-4])
                    for paths in pdf_path:
                        images = convert_from_path(paths)

                        first_page = 1
                        # total_images = len(images)
                        # last_page = min(9, total_images)
                        second_page = 2
                        image_page = 3

            
                        for i, image in enumerate(images):
                            page_number = i+1
                            if page_number == first_page:
                                output_path = os.path.join("OCR_TMP", f"1_first_page_{files[:-4]}.png")
                                image.save(output_path, "PNG")
                            if page_number == second_page:
                                output_path = os.path.join("OCR_TMP", f"2_second_page_{files[:-4]}.png")
                                image.save(output_path, "PNG")
                            if page_number == image_page:
                                output_path = os.path.join("OCR_TMP", f"3_image_page_{files[:-4]}.png")
                                image.save(output_path, "PNG")
                self.conversion_finished.emit("Ready")
            except Exception as e:
                self.conversion_error.emit(f"Error - {e}")

    def conversion(self):
        pdf_path = self.db.get_filepath_from_innovation_proposal(self.level_data[:-4])
        images = convert_from_path(pdf_path[0])

        first_page = 1
        #total_images = len(images)
        # last_page = min(9, total_images)
        second_page = 2
        image_page = 3

        os.makedirs("OCR_TMP", exist_ok = True)
        for i, image in enumerate(images):
            page_number = i+1
            if page_number == first_page:
                output_path = os.path.join("OCR_TMP", f"1_first_page_{self.level_data[:-4]}.png")
                image.save(output_path, "PNG")
            if page_number == second_page:
                output_path = os.path.join("OCR_TMP", f"2_second_page_{self.level_data[:-4]}.png")
                image.save(output_path, "PNG")
            if page_number == image_page:
                output_path = os.path.join("OCR_TMP", f"3_image_page_{self.level_data[:-4]}.png")
                image.save(output_path, "PNG")

if __name__ == "__main__":
    start = Conversion_Thread()
    start.conversion_finished.connect(lambda ad: print(f"conversion_finished {ad}"))
    start.conversion_error.connect(lambda dd: print(f"Сигнал conversion_error {dd}"))

    start.run()
