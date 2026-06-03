from PyQt5.QtCore import QThread, pyqtSignal
from OCR.conversion import Conversion

class Conversion_Thred(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.conversion = Conversion()

    def run(self):
        try:
            self.conversion.pdf_png()
            self.signal.emit(f"Шаг {i+1} завершен")
            self.signal.emit("ГОТОВО!")
            self.finished.emit()
        except Exception as e:
            self.signal.emmit(f"Error {e}")
