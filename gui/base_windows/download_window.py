from PyQt5.QtWidgets import QWidget

from gui.ui.download import Ui_Form
from gui.option_windows.edit_window import Edit_window

from handlers.base.download.download_main import Download

class Download_window(QWidget):
    def __init__(self, top_window, db, model):
        super().__init__()
        self.top_window = top_window
        self.db = db
        self.model = model

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals()
        return self
    
    def signals(self):
        self.handler = Download(self.top_window, self, self.db, self.model)
        self.edit = Edit_window(self)

        #Распознование текста
        self.gui.pushButton.clicked.connect(self.handler.download)

        #Семантический поиск (Наименование + Описание)
        self.gui.pushButton_2.clicked.connect(self.handler.check)

        #Исправление распознанного текста
        self.gui.pushButton_3.clicked.connect(self.handler.edit)

        #Загрузка в БД
        #self.gui.pushButton_.clicked.connect(self.handler.write)

        #Заключение
        #self.parent.gui.reply_pushButton.connect(self.handler.conclution)




