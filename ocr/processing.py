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

        for i, image in enumerate(sorted(paths)):
            process_image = cv2.imread(image)
            gray = cv2.cvtColor(process_image, cv2.COLOR_BGR2GRAY)
            _, black_white = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            result = cv2.bitwise_not(black_white)
            cropped = result[1470:1600, 0:2000]
            final_path = os.path.join("OCR_TMP", f"page_{i+1}_processed.png")
            cv2.imwrite(final_path, cropped)
        
        result = "Обработка завершена."
        return result

if __name__ == "__main__":
    start = Processing_Thread()
    start.processing_finished.connect(lambda dd: print(f"processing_finished {dd}"))
    start.processing_error.connect(lambda df: print(f"processing_error {df}"))
    start.run()
