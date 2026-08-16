from PyQt5.QtWidgets import QFileDialog

from handlers.engine.image_searching.image_searching import Image_searching_thread

from log.logging import logger

from data.messagebox import critical_message

class Image_searching:

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None

    def start(self):
        image_path = self.load_image()
        if image_path != None:
            self.searching_thread(image_path)
        else:
            critical_message(self.parent, f"Выберите изображение")

    def load_image(self):
        image_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if image_path:
            return image_path
        else:
            return None

    def searching_thread(self, image_path):
        self.thread = Image_searching_thread(image_path)
        self.thread.image_searching_finished.connect(self.searching_finished)
        self.thread.image_searching_error.connect(self.searhing_error)
        self.thread.start()

    def searching_finished(self, embedding):
        self.thread.deleteLater()
        logger.error(f"IMAGE SEARCHING | FINISHED - SUCCESS")

    def searhing_error(self, error):
        self.thread.deleteLater()
        logger.error(f"IMAGE SEARCHING | FINISHED - ERROR: {error}")
