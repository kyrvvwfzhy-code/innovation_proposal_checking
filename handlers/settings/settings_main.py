from PyQt5.QtWidgets import QFileDialog
from pdf2image import convert_from_path
import cv2
import pytesseract
import os

class Settings:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
    
    def main(self):
        filename_list = self.load_file()
        self.conversion(filename_list)
        self.processing()
        self.recognition(filename_list)

    def load_file(self):
        folder_path = QFileDialog.getExistingDirectory(
            None, 
            "Выберите папку",
            "",
            QFileDialog.ShowDirsOnly
        )

        if folder_path:
            filename_list = os.listdir(folder_path)
            for filenames in filename_list:
                file_paths = os.path.join(folder_path, filenames)
                self.db.add_innovation_proposal(filenames[:-4], file_paths)

        return filename_list

    def conversion(self, filename_list):
        os.makedirs("OCR_TMP", exist_ok = True)

        for files in filename_list:
            pdf_path = self.db.get_loaded_ip(files[:-4])
            for paths in pdf_path:
                images = convert_from_path(paths)

                first_page = 1
                total_images = len(images)
                last_page = min(9, total_images)

    
                for i, image in enumerate(images):
                    page_number = i+1
                    if page_number == first_page:
                        output_path = os.path.join("OCR_TMP", f"1_first_page_{files[:-4]}.png")
                        image.save(output_path, "PNG")
                    if page_number == last_page:
                        output_path = os.path.join("OCR_TMP", f"2_last_page_{files[:-4]}.png")
                        image.save(output_path, "PNG")
    
    def processing(self):
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            paths = []
            for filename in os.listdir(folder_path):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    paths.append(full_path)

        file = sorted(paths)
        for file_path in file:
            filename = os.path.basename(file_path) 
            if filename.startswith('1'):
                self.process_first_page(file_path)
            elif filename.startswith('2'):
                self.process_last_page(file_path)
            
    def process_first_page(self, file_path):
        filename = os.path.basename(file_path)
        process_image = cv2.imread(file_path)
        gray = cv2.cvtColor(process_image, cv2.COLOR_BGR2GRAY)
        _, black_white = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        result = cv2.bitwise_not(black_white)
        self.process_registered(result, filename)
        self.process_name(result, filename)

    def process_registered(self,result, filename):
        cropped = result[670:920, 100:750]
        final_path = os.path.join("OCR_TMP", f"{filename[:-4]}_registered_processed.png")
        cv2.imwrite(final_path, cropped)

    def process_name(self, result, filename):
        cropped = result[1470:1600, 0:2000]
        final_path = os.path.join("OCR_TMP", f"2_{filename[2:][:-4]}_name_processed.png")
        cv2.imwrite(final_path, cropped)

    def process_last_page(self, file_path):
        filename = os.path.basename(file_path)
        process_image = cv2.imread(file_path)
        gray = cv2.cvtColor(process_image, cv2.COLOR_BGR2GRAY)
        _, black_white = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        result = cv2.bitwise_not(black_white)
        cropped = result[658:715, 0:2000]
        final_path = os.path.join("OCR_TMP", f"{filename[:-4]}_author_processed.png")
        cv2.imwrite(final_path, cropped)

    def recognition(self, filename_list):
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            paths = []
            for filename in os.listdir(folder_path):
                if filename.endswith('_processed.png'):
                    full_path = os.path.join(folder_path, filename)
                    if os.path.isfile(full_path):
                        paths.append(full_path)
        
        file = sorted(paths)
        
        # Словарь для хранения данных по каждому файлу
        file_data = {}
        
        for file_path in file:
            filename = os.path.basename(file_path)
            
            # Извлекаем базовое имя файла (без суффиксов)
            if '_registered_processed.png' in filename:
                base_name = filename.replace('_registered_processed.png', '')
                registered = pytesseract.image_to_string(file_path, lang='rus+eng')
                if base_name not in file_data:
                    file_data[base_name] = {}
                file_data[base_name]['registered'] = registered
                
            elif '_name_processed.png' in filename:
                base_name = filename.replace('_name_processed.png', '')
                # Убираем "2_" если есть
                if base_name.startswith('2_'):
                    base_name = base_name[2:]
                name = pytesseract.image_to_string(file_path, lang='rus+eng')
                if base_name not in file_data:
                    file_data[base_name] = {}
                file_data[base_name]['name'] = name
                
            elif '_author_processed.png' in filename:
                base_name = filename.replace('_author_processed.png', '')
                author = pytesseract.image_to_string(file_path, lang='rus+eng')
                if base_name not in file_data:
                    file_data[base_name] = {}
                file_data[base_name]['author'] = author
        
        # Теперь обрабатываем собранные данные
        for base_name, data in file_data.items():
            # Проверяем, что все данные собраны
            if 'registered' in data and 'name' in data and 'author' in data:
                # Добавляем в базу данных с правильными параметрами
                # Приведите параметры в соответствие с вашей БД
                self.db.add_key_information(
                    base_name, 
                    data['registered'], 
                    data['name'], 
                    data['author']
            )