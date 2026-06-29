from PyQt5.QtWidgets import QFileDialog
import os


class Settings:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def data_download(self):
        self.get_files()
    
    def get_files(self):
        folder_path = QFileDialog.getExistingDirectory(
            None, 
            "Выберите папку",
            "",
            QFileDialog.ShowDirsOnly
        )

        if folder_path:
            el = os.listdir(folder_path)
            print(el)
            for elements in el:
                file_path = os.path.join(folder_path, elements)
                print(file_path)
            
                