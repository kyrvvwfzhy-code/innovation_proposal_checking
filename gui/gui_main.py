from PyQt5.QtWidgets import QWidget

from gui.top_window import Top_window
from gui.base_window import Base_window
from gui.data_window import Data_window
from gui.search_window import Search_window
from gui.settings_window import Settings_window
from log.logging import logger

class GUI_main(QWidget):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.init()
    
    def init(self):
        self.top_window = Top_window(self.parent)
        self.base_window = Base_window(self.db)
        self.data_window = Data_window(self.db)
        self.search_window = Search_window(self.db)
        self.settings_window = Settings_window(self.db)
        self.top_window_config()

    def top_window_config(self):
        self.top_window.gui.stackedWidget.addWidget(self.base_window.open())
        self.top_window.gui.stackedWidget.addWidget(self.data_window.open())
        self.top_window.gui.stackedWidget.addWidget(self.search_window.open())
        self.top_window.gui.stackedWidget.addWidget(self.settings_window.open())

        self.top_window.gui.pushButton.clicked.connect(self.goto_base_window)
        self.top_window.gui.pushButton_1.clicked.connect(self.goto_data_window)
        self.top_window.gui.pushButton_2.clicked.connect(self.goto_search_window)
        self.top_window.gui.pushButton_3.clicked.connect(self.goto_settings_window)

    def goto_base_window(self):
        logger.info("OPEN - base_window")
        self.top_window.gui.stackedWidget.setCurrentIndex(0)
    
    def goto_data_window(self):
        logger.info("OPEN - data_window")
        self.top_window.gui.stackedWidget.setCurrentIndex(1)
    
    def goto_search_window(self):
        logger.info("OPEN - search_window")
        self.top_window.gui.stackedWidget.setCurrentIndex(2)
    
    def goto_settings_window(self):
        logger.info("OPEN - settings_window")
        self.top_window.gui.stackedWidget.setCurrentIndex(3)