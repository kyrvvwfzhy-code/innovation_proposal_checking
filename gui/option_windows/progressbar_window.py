from PyQt5.QtWidgets import QWidget

from gui.ui.progressbar import Ui_Form

from handlers.options.progressbar.progressbar_main import Progressbar

class Progressbar_window(QWidget):
    def __init__(self):
        super().__init__()

    def open(self, target):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals(target)
        self.show()

    def signals(self, target):
        self.handler = Progressbar(self, target)
