from PyQt5.QtWidgets import QWidget

from gui.ui.settings import Ui_Form

from gui.option_windows.prompt_window import Prompt_window
from gui.option_windows.progressbar_window import Progressbar_window

from handlers.base.settings.settings_main import Settings

class Settings_window(QWidget):
    def __init__(self, db, model):
        super().__init__()
        self.db = db
        self.model = model

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals()
        return self
    
    def signals(self):
        self.progressbar = Progressbar_window()
        self.prompt = Prompt_window(self.db)
        
        self.handler = Settings(self, self.db, self.model)

        # Загрузка массивистых данных
        self.gui.pushButton.clicked.connect(self.handler.download)

        # Настройки инструкций LLM модели
        self.gui.pushButton_2.clicked.connect(self.handler.prompt)

