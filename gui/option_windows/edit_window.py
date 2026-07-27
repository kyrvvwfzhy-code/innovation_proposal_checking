from PyQt5.QtWidgets import QWidget

from gui.ui.edit import Ui_Form

from handlers.options.edit.edit_main import Edit

class Edit_window(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def open(self, db, filename, registered, name, description):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.signals(db, filename, registered, name, description)
        self.show()

    def signals(self, db, filename, registered, name, description):
        self.handler = Edit(self.parent, db, filename, registered, name, description)