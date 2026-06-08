from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os

from db.database import DataBase
from ocr.ocr_main import OCR_main

class Load_file:
    def __init__(self, parent):
        self.parent = parent
        self.db = DataBase()
        self.ocr = OCR_main(parent)
    
    def start(self):
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
        if hasattr(self, 'parent') and hasattr(self.parent, 'gui') and hasattr(self.parent.gui, 'label_4') and self.parent.gui.label_4 is not None:
            self.parent.gui.label_4.setText(filename)
        else:
            self.parent.gui.label_4.setText(filename)

        self.parent.gui.label_4.show()
        exist = self.db.add_rational_proposal(filename[:-4], file_path)
        if exist != None:
            self.logg_box(exist)
        else:
            self.ocr.start_ocr()
        
    
    def logg_box(self, exist):
        QMessageBox.information(self.parent, "Информация", exist)

    