from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import os

class Processing_Thread(QThread):
    processing_finished = pyqtSignal(str)
    processing_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            result = self.processing()
            self.processing_finished.emit(result)
        except Exception as e:
            self.processing_error.emit(f"Error - {e}")
            
    def processing(self):
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            paths = []
            for filename in os.listdir(folder_path):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    paths.append(full_path)

        file = sorted(paths)
        self.process_first_page(file)
        self.process_last_page(file)

    def process_first_page(self, file):
        image = file[0]
        filename = os.path.basename(image)
        process_image = cv2.imread(image)
        gray = cv2.cvtColor(process_image, cv2.COLOR_BGR2GRAY)
        _, black_white = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        result = cv2.bitwise_not(black_white)
        self.process_registered(result, filename)
        self.process_name(result, filename)

    def process_registered(self,result, filename):
        cropped = result[670:920, 100:750]
        final_path = os.path.join("OCR_TMP", f"{filename}_registered_processed.png")
        cv2.imwrite(final_path, cropped)

    def process_name(self, result, filename):
        cropped = result[1470:1600, 0:2000]
        final_path = os.path.join("OCR_TMP", f"2_{filename[2:]}_name_processed.png")
        cv2.imwrite(final_path, cropped)
        
    def process_last_page(self, file):
        image = file[1]
        filename = os.path.basename(image)
        process_image = cv2.imread(image)
        gray = cv2.cvtColor(process_image, cv2.COLOR_BGR2GRAY)
        _, black_white = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        result = cv2.bitwise_not(black_white)
        cropped = result[658:715, 0:2000]
        final_path = os.path.join("OCR_TMP", f"{filename}_author_processed.png")
        cv2.imwrite(final_path, cropped)

if __name__ == "__main__":
    start = Processing_Thread()
    start.processing_finished.connect(lambda dd: print(f"processing_finished {dd}"))
    start.processing_error.connect(lambda df: print(f"processing_error {df}"))
    start.run()
