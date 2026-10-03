from PyQt5.QtWidgets import QWidget

from gui.ui.search import Ui_Form

from handlers.base.search.search_main import Search

class Search_window(QWidget):
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
        self.handler = Search(self, self.db, self.model)

        #Семантический поиск (Наименования, Описание, Наименование + Описание)
        self.gui.pushButton.clicked.connect(self.handler.search_by_text)

        #Поиск по изображению
        self.gui.pushButton_2.clicked.connect(self.handler.search_by_image)

