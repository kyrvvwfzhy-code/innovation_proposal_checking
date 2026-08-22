from handlers.engine.Image_Searching.load_image import Load_image
from handlers.engine.Image_Searching.vectorization import Vectorization_thread
from handlers.engine.Image_Searching.searching import Searching_thread

from data.output_message import image_conclusion_output
from log.logging import logger

import subprocess

class Image_searching_main:

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.thread = None

    def start(self):
        logger.info(f"IMAGE SEARCHING | STARTING...")
        self.load_image = Load_image(self.parent)
        self.image_path = self.load_image.start()
        if self.image_path != None:
            logger.info(f"IMAGE SEARCHING | FILE - \"{self.image_path}\" selected")
            self.vectorization_thread()

    def vectorization_thread(self):
        logger.error(f"IMAGE SEARCHING | START - Vectorization")
        self.thread = Vectorization_thread(self.image_path)
        self.thread.vectorization_finished.connect(self.vectorization_finished)
        self.thread.vectorization_error.connect(self.vectorization_error)
        self.thread.start()

    def vectorization_finished(self, image_embedding):
        self.thread.deleteLater()
        logger.error(f"IMAGE SEARCHING | FINISHED - Vectorization (SUCCESS)")
        self.searching_thread(image_embedding)

    def vectorization_error(self, error):
        self.thread.deleteLater()
        logger.error(f"IMAGE SEARCHING | FINISHED - Vectorization (ERROR): {error}")
        
    def searching_thread(self, image_embedding):
        logger.info(f"IMAGE SEARCHING | START - Searching")
        db_embeddings = self.db.get_innovation_proposal_embeddings("image")
        self.thread = Searching_thread(image_embedding, db_embeddings)
        self.thread.image_searching_finished.connect(self.searching_finished)
        self.thread.image_searching_error.connect(self.searhing_error)
        self.thread.start()

    def searching_finished(self, data):
        self.thread.deleteLater()
        logger.info(f"IMAGE SEARCHING | FINISHED - Searching (SUCCESS)")
        image_conclusion = image_conclusion_output(data['name'], data['similarity'])
        self.parent.gui.plainTextEdit_3.setPlainText(image_conclusion)

        subprocess.call(['xdg-open', self.image_path])
        subprocess.call(['xdg-open', data['filepath']])

    def searhing_error(self, error):
        self.thread.deleteLater()
        logger.error(f"IMAGE SEARCHING | FINISHED - ERROR: {error}")
