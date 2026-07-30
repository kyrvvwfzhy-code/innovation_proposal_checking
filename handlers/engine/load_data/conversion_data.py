from PyQt5.QtCore import QThread, pyqtSignal
from pdf2image import convert_from_path
import os

class Conversion_data_Thread(QThread):
    conversion_data_finished = pyqtSignal(str)
    conversion_data_error = pyqtSignal(str)
    
    def __init__(self, db, filename_list):
        super().__init__()
        self.db = db
        self.filename_list = filename_list

    def run(self):
        try:
            os.makedirs("OCR_TMP", exist_ok = True)

            for files in self.filename_list:
                pdf_path = self.db.get_path_from_innovation_proposal(files[:-4])
                for paths in pdf_path:
                    images = convert_from_path(paths)

                    first_page = 1
                    # total_images = len(images)
                    # last_page = min(9, total_images)
                    second_page = 2

        
                    for i, image in enumerate(images):
                        page_number = i+1
                        if page_number == first_page:
                            output_path = os.path.join("OCR_TMP", f"1_first_page_{files[:-4]}.png")
                            image.save(output_path, "PNG")
                        if page_number == second_page:
                            output_path = os.path.join("OCR_TMP", f"2_second_page_{files[:-4]}.png")
                            image.save(output_path, "PNG")
            self.conversion_data_finished.emit("Ready")
        except Exception as e:
            self.conversion_data_error.emit(f"Error - {e}")