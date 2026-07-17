from PyQt5.QtWidgets import QWidget

from gui.ui.top import Ui_Form

class Top_window(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init()

    def init(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)