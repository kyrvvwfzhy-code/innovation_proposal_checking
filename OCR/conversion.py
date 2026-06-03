from pdf2image import convert_from_path
import os
from DATABASE.database import DataBase

class Conversion:
    def __init__(self):
        self.db = DataBase()

    def pdf_png(self):
        pdf_path = self.db.get_loaded_rp()
        images = convert_from_path(pdf_path[1])

        os.makedirs("OCR_TMP", exist_ok = True)
        for i, image in enumerate(images):
            output_path = os.path.join("OCR_TMP", f"page_{pdf_path[0]}_{i+1}.png")
            image.save(output_path, "PNG")

if __name__ == "__main__":
    start = Conversion()