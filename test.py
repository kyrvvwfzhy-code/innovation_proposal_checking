import sys
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QApplication

# Простой тестовый поток
class TestThread(QThread):
    finished = pyqtSignal()
    
    def run(self):
        print("  Поток запущен")
        import time
        time.sleep(1)
        print("  Поток завершён")
        self.finished.emit()

class OCR_main:
    def __init__(self):
        print("1. Инициализация")
        self.thread = None
        self.start_ocr()
    
    def start_ocr(self):
        print("2. Запуск потока")
        self.thread = TestThread()
        self.thread.finished.connect(self.conversion_finished)
        self.thread.start()
    
    def conversion_finished(self):
        print("3. Сигнал получен")
        self.thread.deleteLater()
        self.thread = None
        print("4. Очистка завершена")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("0. Запуск приложения")
    ocr = OCR_main()
    print("5. Выход")
    sys.exit(app.exec_())