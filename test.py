import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget

# ========== ПОТОК ==========
class WorkerThread(QThread):
    signal = pyqtSignal(str)  # Сигнал для отправки сообщений
    
    def run(self):
        for i in range(5):
            time.sleep(1)
            self.signal.emit(f"Шаг {i+1} завершен")
        self.signal.emit("ГОТОВО!")

# ========== ГЛАВНОЕ ОКНО ==========
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Потоки в PyQt")
        self.setGeometry(300, 300, 400, 300)
        
        # Кнопка
        self.btn = QPushButton("Запустить поток")
        self.btn.clicked.connect(self.start_thread)
        
        # Поле для вывода
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.btn)
        layout.addWidget(self.log)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def start_thread(self):
        self.btn.setEnabled(False)
        self.log.append("🚀 Запускаю поток...")
        
        # Создаем и запускаем поток
        self.thread = WorkerThread()
        self.thread.signal.connect(self.on_message)
        self.thread.start()
    
    def on_message(self, msg):
        self.log.append(msg)
        
        if msg == "ГОТОВО!":
            self.btn.setEnabled(True)

# ========== ЗАПУСК ==========
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())