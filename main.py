import torch
from PyQt5.QtWidgets import QApplication, QMainWindow

from db.database import DataBase
from gui.gui_main import GUI_main

from log.logging import logger
import sys

class IPC(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()
    
    def init(self):
        logger.info("APPLICATION - Running...")
        self.db = DataBase()
        self.db.create_tables()
        self.main = GUI_main(self, self.db)
        self.setWindowTitle("Проверка рационализаторских предложений")
        self.setFixedSize(1104, 701)
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()

def start_app():
    App = QApplication(sys.argv)
    Window = IPC()
    Window.show() 
    sys.exit(App.exec_())

if __name__ == "__main__":
    start_app()