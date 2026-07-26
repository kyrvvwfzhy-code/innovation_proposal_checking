from PyQt5.QtWidgets import QWidget
from gui.ui.edit import Ui_Form

class Edit_window(QWidget):
    def __init__(self):
        super().__init__()

    def open(self):
        self.gui = Ui_Form()
        self.gui.setupUi(self)
        self.show()
    
    def filling_data(self, registered, name):
        self.gui.lineEdit.setText(registered)
        self.gui.lineEdit_2.setText(name)

    def save_data(self):
        edit_registered = self.gui.lineEdit.text().strip()
        edit_name = self.gui.lineEdit_2.text().strip()
        return edit_registered, edit_name
