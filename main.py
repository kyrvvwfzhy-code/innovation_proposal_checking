import torch
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from db.database import DataBase
from gui.gui_main import GUI_main

class IPC(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()
    
    def init(self):
        self.db = DataBase()
        self.db.create_tables()
        self.main = GUI_main(self)

def start_app():
    App = QApplication(sys.argv)
    Window = IPC()
    Window.show() 
    sys.exit(App.exec_())

if __name__ == "__main__":
    start_app()