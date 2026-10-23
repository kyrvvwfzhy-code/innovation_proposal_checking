from handlers.engine.Image_Searching.load_image import Load_image
from handlers.engine.Image_Searching.vectorization import Vectorization_thread
from handlers.engine.Image_Searching.searching import Searching_thread

from data.output_message import image_conclusion_output
from log.logging import logger

import subprocess
import sys
import os

class Image_searching_main:

    def __init__(self, parent, db, image_encoder_model):
        self.parent = parent
        self.db = db
        self.image_encoder_model = image_encoder_model
        self.thread = None

    def start(self):
        logger.info(f"IMAGE SEARCHING | STARTING...")
        self.clear_fields()
        
        self.load_image = Load_image(self.parent)
        self.image_path = self.load_image.start()
        if self.image_path != None:
            logger.info(f"IMAGE SEARCHING | FILE - \"{self.image_path}\" selected")
            self.vectorization_thread()
            self.search_buttons_status(bool = False)
        else:
            logger.info("IMAGE SEARCHING | FILE - image not selected")
            pass

    def vectorization_thread(self):
        logger.info(f"IMAGE SEARCHING | START - Vectorization")
        self.thread = Vectorization_thread(self.image_path, self.image_encoder_model)
        self.thread.vectorization_finished.connect(self.vectorization_finished)
        self.thread.vectorization_error.connect(self.vectorization_error)
        self.thread.start()

    def vectorization_finished(self, image_embedding):
        self.thread.deleteLater()
        logger.info(f"IMAGE SEARCHING | FINISHED - Vectorization (SUCCESS)")
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
        self.parent.gui.textBrowser_3.setHtml(image_conclusion)

        if sys.platform == 'win32':
            os.startfile(self.image_path)
            os.startfile(data['filepath'])
        else:
            subprocess.call(['xdg-open', self.image_path])
            subprocess.call(['xdg-open', data['filepath']])
            
        logger.info(f"IMAGE SEARCHING | SUCCESSFULL FINISHED")
        self.search_buttons_status(bool = True)

    def searhing_error(self, error):
        self.thread.deleteLater()
        logger.error(f"IMAGE SEARCHING | FINISHED - ERROR: {error}")
        self.search_buttons_status(bool = True)

    def search_buttons_status(self, bool):
        self.parent.gui.pushButton.setEnabled(bool)
        self.parent.gui.pushButton_2.setEnabled(bool)

    def clear_fields(self):
        self.parent.gui.plainTextEdit.clear()
        self.parent.gui.plainTextEdit_2.clear()
        self.parent.gui.textBrowser_3.clear()

