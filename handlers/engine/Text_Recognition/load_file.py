from PyQt5.QtWidgets import QFileDialog

from data.messagebox import critical_message

import os
import shutil
from pathlib import Path

class Load_file:
    def __init__(self, db, level, parent = None):
        self.parent = parent
        self.db = db
        self.level = level
        self.app_dir = Path.home() / "ipc_app"
        self.app_dir.mkdir(parents = True, exist_ok = True)
        self.proposals = self.app_dir / "proposals"
        self.proposals.mkdir(parents=True, exist_ok=True)
    
    def start(self):
        if self.level == "download":

            file_path, _ = QFileDialog.getOpenFileName(self.parent,
                                                    "Выберите файл",
                                                    "",
                                                    "(*.pdf)"
                                                    )

            if file_path:
                filename = os.path.basename(file_path)
                new_file_path = self.proposals / filename
                shutil.copy(file_path, new_file_path)
                result = self.create_filename_label(filename, new_file_path)
            else:
                result = None
            return result
        
        elif self.level == "settings":
            try:
                folder_path = QFileDialog.getExistingDirectory(
                    None, 
                    "Выберите папку",
                    "",
                    QFileDialog.ShowDirsOnly
                )

                if folder_path:
                    exist_files = []
                    filename_list = sorted(os.listdir(folder_path))
                    for filenames in filename_list:
                        new_file_path = self.proposals / filenames
                        src = Path(folder_path) / filenames
                        shutil.copy(src, new_file_path)
                        exist = self.db.add_innovation_proposal(filenames[:-4], str(new_file_path))
                        if exist == True:
                            exist_files.append(filenames)
                    for files in exist_files:
                        critical_message(self.parent, f"Документ {files} уже выгружен")
                        filename_list.remove(files)
                    return filename_list
                else:
                    return None
                
            except Exception as e:
                return f"Error - {e}"
    
    def create_filename_label(self, filename, file_path):
        if hasattr(self, 'parent') and hasattr(self.parent, 'gui') and hasattr(self.parent.gui, 'label_4') and self.parent.gui.label_4 is not None:
            self.parent.gui.label_4.setText(filename)

        self.parent.gui.label_4.show()
        return self.check_exist(filename, file_path)


    def check_exist(self, filename, file_path):
        exist = self.db.add_innovation_proposal(filename[:-4], str(file_path))
        if exist == True:
            return False
        else:
            return filename

    