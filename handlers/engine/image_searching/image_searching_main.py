from PyQt5.QtWidgets import QFileDialog
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
from pdf2image import convert_from_path
import os

class Image_serching_main:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

    def start(self):
        file_path = self.load_data()
        self.recognition(file_path)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self.parent,
                                                           "Выберите файл",
                                                           "",
                                                           "(*.png)"
                                                           )
        
        if file_path:
            filename = os.path.basename(file_path)
            result = filename
        else:
            result = None
            return result
                    
        return result

    def recognition(self, file_path):
        processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
        image = Image.open(file_path)
        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(**inputs, max_new_tokens=200)
        description = processor.decode(out[0], skip_special_tokens=True)

        print(description)