from PyQt5.QtWidgets import QFileDialog
import os

class Load_files:
        def __init__(self, db):
            self.db = db
            
        def start(self):
            try:
                folder_path = QFileDialog.getExistingDirectory(
                    None, 
                    "Выберите папку",
                    "",
                    QFileDialog.ShowDirsOnly
                )

                if folder_path:
                    filename_list = sorted(os.listdir(folder_path))
                    for filenames in filename_list:
                        file_paths = os.path.join(folder_path, filenames)
                        self.db.add_innovation_proposal(filenames[:-4], file_paths)

                return filename_list
                
            except Exception as e:
                return f"Error - {e}"