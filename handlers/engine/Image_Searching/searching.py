from PyQt5.QtCore import QThread, pyqtSignal

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Searching_thread(QThread):
    image_searching_finished = pyqtSignal(dict)
    image_searching_error = pyqtSignal(str)

    def __init__(self, image_embedding, db_embeddings):
        super().__init__()
        self.image_embedding = image_embedding
        self.db_embeddings = db_embeddings

    def run(self):
        try:
            names = [item[0] for item in self.db_embeddings]
            embedding_image = [item[1] for item in self.db_embeddings]
            filepath = [item[2] for item in self.db_embeddings]
            similarities_image = cosine_similarity([self.image_embedding], embedding_image)[0]

            max_index = np.argmax(similarities_image)

            data = {
                'name': names[max_index],
                'similarity': float(similarities_image[max_index]),
                'filepath': filepath[max_index]
            }

            self.image_searching_finished.emit(data)

        except Exception as e:
            self.image_searching_error.emit(f"Error - {e}")

   
