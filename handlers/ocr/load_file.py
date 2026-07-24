from PyQt5.QtWidgets import QFileDialog
import os
from data.messagebox import critical_message

class Load_file:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
    
    def start(self):
        file_path, _ = QFileDialog.getOpenFileName(self.parent,
                                                   "Выберите файл",
                                                   "",
                                                   "(*.pdf)"
                                                   )

        if file_path:
            filename = os.path.basename(file_path)
            result = self.create_filename_label(filename, file_path)
        else:
            result = None
            return result
            
        return result
    
    def create_filename_label(self, filename, file_path):
        if hasattr(self, 'parent') and hasattr(self.parent, 'gui') and hasattr(self.parent.gui, 'label_4') and self.parent.gui.label_4 is not None:
            self.parent.gui.label_4.setText(filename)
        else:
            self.parent.gui.label_4.setText(filename)

        self.parent.gui.label_4.show()
        exist = self.db.add_innovation_proposal(filename[:-4], file_path)

        if exist != None:
            critical_message(self.parent, "Документ уже выгружен")
            return False
        else:
            return True

    