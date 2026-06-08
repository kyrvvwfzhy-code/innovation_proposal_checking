from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from db.database import DataBase
from gui.gui import Ui_MainWindow

from handlers.load_file import Load_file

class RPC(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init()
    
    def init(self):
        self.db = DataBase()
        self.db.create_tables()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.handlers()
    
    def handlers(self):
        self.load = Load_file(self)
        self.gui.pushButton.clicked.connect(self.load.start)
        # self.gui.pushButton_2.clicked.connect()

def start_app():
    App = QApplication(sys.argv)
    Window = RPC()
    Window.show()
    sys.exit(App.exec_())

if __name__ == "__main__":
    start_app()