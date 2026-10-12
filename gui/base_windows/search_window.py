from PyQt5.QtWidgets import QWidget

from gui.ui.search import Ui_Form

from handlers.base.search.search_main import Search

class Search_window(QWidget):
    def __init__(self, db, image_encoder_model, text_embedding_model, instruct_model):
        super().__init__()
        self.db = db
        self.image_encoder_model = image_encoder_model
        self.text_embedding_model = text_embedding_model
        self.instruct_model = instruct_model

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals()
        return self

    def signals(self):
        self.handler = Search(self, self.db, self.image_encoder_model, self.text_embedding_model, self.instruct_model)

        #Семантический поиск (Наименования, Описание, Наименование + Описание)
        self.gui.pushButton.clicked.connect(self.handler.search_by_text)

        #Поиск по изображению
        self.gui.pushButton_2.clicked.connect(self.handler.search_by_image)

