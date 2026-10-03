from PyQt5.QtWidgets import QWidget

from gui.base_windows.top_window import Top_window
from gui.base_windows.download_window import Download_window
from gui.base_windows.journal_window import Journal_window
from gui.base_windows.search_window import Search_window
from gui.base_windows.settings_window import Settings_window

from log.logging import logger

class GUI_main(QWidget):
    def __init__(self, parent, db, model):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.model = model
        self.init()
    
    def init(self):
        self.top_window = Top_window(self.parent, self.db)
        self.download_window = Download_window(self.top_window, self.db, self.model)
        self.journal_window = Journal_window(self.db)
        self.search_window = Search_window(self.db, self.model)
        self.settings_window = Settings_window(self.db, self.model)
        self.top_window_signals()

    def top_window_signals(self):
        self.top_window.gui.stackedWidget.addWidget(self.download_window.open())
        self.top_window.gui.stackedWidget.addWidget(self.journal_window.open())
        self.top_window.gui.stackedWidget.addWidget(self.search_window.open())
        self.top_window.gui.stackedWidget.addWidget(self.settings_window.open())

        self.top_window.gui.pushButton.clicked.connect(self.goto_download_window)
        self.top_window.gui.pushButton_1.clicked.connect(self.goto_journal_window)
        self.top_window.gui.pushButton_2.clicked.connect(self.goto_search_window)
        self.top_window.gui.pushButton_3.clicked.connect(self.goto_settings_window)

    def goto_download_window(self):
        logger.info("MAIN | OPEN - download_window")
        self.top_window.gui.stackedWidget.setCurrentIndex(0)
    
    def goto_journal_window(self):
        logger.info("MAIN | OPEN - journal_window")
        self.top_window.gui.stackedWidget.setCurrentIndex(1)
    
    def goto_search_window(self):
        logger.info("MAIN | OPEN - search_window")
        self.top_window.gui.stackedWidget.setCurrentIndex(2)
    
    def goto_settings_window(self):
        logger.info("MAIN | OPEN - settings_window")
        self.top_window.gui.stackedWidget.setCurrentIndex(3)