from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os

from db.database import DataBase

class Load_file:
    def __init__(self, parent):
        self.parent = parent
        self.db = DataBase()
    
    def open_file_manager(self):
        file_path, _ = QFileDialog.getOpenFileName(self.parent,
                                                   "Выберите файл",
                                                   "",
                                                   "(*.pdf)"
                                                   )

        if file_path:
            filename = os.path.basename(file_path)
            self.create_getFile_label(filename, file_path)
        else:
            print("Файл не выбран")
    
    def create_getFile_label(self, filename, file_path):
        if hasattr(self, "label") and self.label is not None:
            self.label.setText(filename)
        else:
            self.label = QtWidgets.QLabel(self.parent)
            self.label.setGeometry(QtCore.QRect(580, 80, 100, 20))
            self.label.setObjectName("Label")
            self.label.setText(filename)

        self.label.show()
        exist = self.db.add_rational_proposal(filename[:-4], file_path)
        if exist != None:
            self.logg_box(exist)
    
    def logg_box(self, exist):
        QMessageBox.information(self.parent, "Информация", exist)

    