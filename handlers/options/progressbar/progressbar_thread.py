from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QLabel
import os

class Progressbar_Thread(QThread):
    progress_update = pyqtSignal(str)
    progress_error = pyqtSignal(str)

    def __init__(self, parent, db, target):
        super().__init__()
        self.parent = parent
        self.db = db
        self.target = target

    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_path)
        self.timer.start(1000)
        self.exec_()

    def check_path(self):
        current_count = self.db.get_ready_innovation_proposal_embeddings()

        progress = int((current_count * 100) / self.target)
        
        if progress > 100:
            progress = 100
        
        self.parent.gui.progressBar.setValue(progress)
        self.parent.gui.label.setText(f"{current_count} из {self.target}")

        if current_count >= self.target:
            self.parent.gui.progressBar.setValue(100)
            self.parent.gui.label.setText(f"✅ ГОТОВО! {current_count} файлов")
            self.timer.stop()
            self.quit()