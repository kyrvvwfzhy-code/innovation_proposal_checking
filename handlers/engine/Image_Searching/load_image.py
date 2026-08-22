from PyQt5.QtWidgets import QFileDialog

from data.messagebox import critical_message

class Load_image:
    def __init__(self, parent = None):
        self.parent = parent

    def start(self):
        try:
            image_path, _ = QFileDialog.getOpenFileName(
                        self.parent,
                        "Выберите изображение",
                        "",
                        "Изображения (*.png *.jpg *.jpeg *.bmp *.webp)"
                    )
            if image_path:
                return image_path
            else:
                critical_message(self.parent, f"Выберите изображение")
                return None
        except Exception as e:
            return e
