from PyQt5.QtWidgets import QWidget

from gui.base_window import Base_window
from gui.data_window import Data_window
from gui.settings_window import Settings_window

class GUI_main(QWidget):
    def __init__(self, parent, db):
        super().__init__()
        self.parent = parent
        self.db = db
        self.init()
    
    def init(self):
        self.base_window = Base_window(self.parent, self.db)
        self.data_window = Data_window(self.db)
        self.settings_window = Settings_window(self.db)
        self.base_window.gui.pushButton_3.clicked.connect(self.data_window.open)
        self.base_window.gui.pushButton_5.clicked.connect(self.settings_window.open)