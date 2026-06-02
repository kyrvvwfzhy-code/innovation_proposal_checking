from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog 
import os

from DATABASE.database import DataBase

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
        self.label = QtWidgets.QLabel(self.parent)
        self.label.setGeometry(QtCore.QRect(580, 80, 100, 20))
        self.label.setObjectName("Label")
        self.label.setText(filename)
        self.label.show()
        self.db.add_rational_proposal(filename,file_path)