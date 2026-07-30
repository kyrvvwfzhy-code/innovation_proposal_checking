from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import os

class Processing_data_Thread(QThread):
    processing_data_finished = pyqtSignal(str)
    processing_data_error = pyqtSignal(str)
    
    def run(self):
        try:
            folder_path = "OCR_TMP"
            if os.path.exists(folder_path):
                paths = []
                for filename in os.listdir(folder_path):
                    full_path = os.path.join(folder_path, filename)
                    if os.path.isfile(full_path):
                        paths.append(full_path)

            file = sorted(paths)
            for file_path in file:
                filename = os.path.basename(file_path) 
                if filename.startswith('1'):
                    self.process_first_page(file_path)
                elif filename.startswith('2'):
                    self.process_second_page(file_path)
                    
            self.processing_data_finished.emit("Ready")
        except Exception as e:
            self.processing_data_error.emit(f"Error - {e}")
            
    def process_first_page(self, file_path):
        filename = os.path.basename(file_path)
        process_image = cv2.imread(file_path)
        gray = cv2.cvtColor(process_image, cv2.COLOR_BGR2GRAY)
        _, black_white = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        result = cv2.bitwise_not(black_white)
        self.process_registered(result, filename)
        self.process_name(result, filename)

    def process_registered(self,result, filename):
        cropped = result[670:920, 100:750]
        final_path = os.path.join("OCR_TMP", f"{filename[:-4]}_registered_processed.png")
        cv2.imwrite(final_path, cropped)

    def process_name(self, result, filename):
        cropped = result[1477:1600, 0:2000]
        final_path = os.path.join("OCR_TMP", f"2_{filename[2:][:-4]}_name_processed.png")
        cv2.imwrite(final_path, cropped)

    def process_second_page(self, file_path):
        filename = os.path.basename(file_path)
        process_image = cv2.imread(file_path)
        gray = cv2.cvtColor(process_image, cv2.COLOR_BGR2GRAY)
        _, black_white = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        result = cv2.bitwise_not(black_white)
        cropped = result[400:1700, 0:2000]
        final_path = os.path.join("OCR_TMP", f"{filename[:-4]}_description_processed.png")
        cv2.imwrite(final_path, cropped)
