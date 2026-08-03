from PyQt5.QtWidgets import QFileDialog
import ollama
import os


class Image_serching_main:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.model_name = "qwen3-vl:latest"

    def start(self):
        file_path = self.load_data()

        if file_path:
            self.recognition(file_path)
        else:
            print("Файл не выбран.")

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.webp)"
        )

        return file_path if file_path else None

    def recognition(self, file_path):
        if not os.path.exists(file_path):
            print("Файл не найден!")
            return

        try:
            response = ollama.chat(
                model=self.model_name,
                think=False,
                keep_alive="30m",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Опиши изображение максимально кратко "
                            "(не более двух предложений). "
                            "Ответ только на русском языке."
                        ),
                        "images": [file_path],
                    }
                ],
                options={
                    "temperature": 0,
                    "num_predict": 100,
                },
            )

            print(response.message.content)

        except Exception as e:
            print("Ошибка:", e)