from PyQt5.QtCore import QThread, pyqtSignal
import pytesseract
import os


class Recognition_data_Thread(QThread):
    recognition_data_finished = pyqtSignal(list)
    recognition_data_error = pyqtSignal(str)

    def __init__(self, db, filename_list):
        super().__init__()
        self.db = db
        self.filename_list = filename_list

    def run(self):
        try:
            folder_path = "OCR_TMP"
            if os.path.exists(folder_path):
                paths = []
                for filename in os.listdir(folder_path):
                    if filename.endswith('_processed.png'):
                        full_path = os.path.join(folder_path, filename)
                        if os.path.isfile(full_path):
                            paths.append(full_path)
            file = sorted(paths)

            result_list = []

            for paths in file:
                if paths.endswith("_registered_processed.png"):
                    registered = pytesseract.image_to_string(paths, lang='rus+eng')
                    result_list.append(registered)
                if paths.endswith("_name_processed.png"):
                    name = pytesseract.image_to_string(paths, lang='rus+eng')
                    result_list.append(name)
                if paths.endswith("_description_processed.png"):
                    description = pytesseract.image_to_string(paths, lang='rus+eng')
                    result_list.append(description)
                
            if registered in result_list and name in result_list and description in result_list:
                total_items = len(result_list)
                items_per_group = total_items // 3
                
                dates = result_list[0:items_per_group]
                names = result_list[items_per_group:items_per_group * 2]
                descriptions = result_list[items_per_group * 2:]
                
                for idx, files in enumerate(self.filename_list):
                    if idx < len(dates):
                        filename = os.path.basename(files)
                    
                        date = self.clean_text(dates[idx])
                        name = self.clean_text(names[idx])
                        description = self.clean_text(descriptions[idx])
                        
                        self.db.add_key_information(
                            filename[:-4], date, name, description)
                        
            result = [names, descriptions]

            self.recognition_data_finished.emit(result)

        except Exception as e:
            self.recognition_data_error.emit(f"Error - {e}")

    def clean_text(self, elements):
        return ' '.join(str(elements).replace('\n', ' ').replace('\x0c', ' ').split()).strip()
        
  