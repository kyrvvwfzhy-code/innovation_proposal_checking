from PyQt5.QtWidgets import QFileDialog
from pdf2image import convert_from_path
import cv2
import pytesseract
from sentence_transformers import SentenceTransformer
import os

class Settings:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
    
    def main(self):
        filename_list = self.load_file()
        self.conversion(filename_list)
        self.processing()
        names = self.recognition(filename_list)
        self.embedding(filename_list, names)

    def load_file(self):
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

        result_list = []

        for paths in file:
            if paths.endswith("_registered_processed.png"):
                registered = pytesseract.image_to_string(paths, lang='rus+eng')
                result_list.append(registered)
            if paths.endswith("_name_processed.png"):
                name = pytesseract.image_to_string(paths, lang='rus+eng')
                result_list.append(name)
            if paths.endswith("_author_processed.png"):
                author = pytesseract.image_to_string(paths, lang='rus+eng')
                result_list.append(author)
            
        if registered in result_list and name in result_list and author in result_list:
            total_items = len(result_list)
            items_per_group = total_items // 3
            
            dates = result_list[0:items_per_group]
            names = result_list[items_per_group:items_per_group * 2]
            authors = result_list[items_per_group * 2:]
            
            for idx, files in enumerate(filename_list):
                if idx < len(dates):
                    filename = os.path.basename(files)
                
                    date = self.clean_text(dates[idx])
                    name = self.clean_text(names[idx])
                    author = self.clean_text(authors[idx])
                    
                    number = 123
                    
                    self.db.add_key_information(
                        filename[:-4], number, date, name, author)
        
        self.clear_folder()
        
        return names

    def clean_text(self, elements):
        return ' '.join(str(elements).replace('\n', ' ').replace('\x0c', ' ').split()).strip()
    
    def embedding(self, filename_list, names):
        model_en = SentenceTransformer('all-MiniLM-L6-v2')
        
        for idx, filename in enumerate(filename_list):
            name = names[idx]
            
            cleaned_name = self.clean_text(name)
            
            embeddings = model_en.encode(cleaned_name)
            new_embedding = embeddings.tolist()
            
            self.db.add_embedding(filename, new_embedding)
            print(f"✅ Эмбеддинг для: {os.path.basename(filename)} → {cleaned_name[:50]}...")
    
    def clear_folder(self):
        folder_path = "OCR_TMP"
        if os.path.exists(folder_path):
            paths = []
            for filename in os.listdir(folder_path):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    paths.append(full_path)
                    os.remove(full_path)