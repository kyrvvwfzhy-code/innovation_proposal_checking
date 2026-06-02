from pdf2image import convert_from_path
import os
from DATABASE.database import DataBase

class Conversion:
    def __init__(self):
        self.db = DataBase()
        self.pdf_png()

    def pdf_png(self):
        pdf_path = self.db.get_loaded_rp()
        images = convert_from_path(pdf_path[1])

        os.makedirs("PDF_IMAGE", exist_ok = True)
        for i, image in enumerate(images):
            output_path = os.path.join("PDF_IMAGE", f"page_{pdf_path[0]}_{i+1}.png")
            image.save(output_path, "PNG")

if __name__ == "__main__":
    start = Conversion()