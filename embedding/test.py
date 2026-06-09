from sentence_transformers import SentenceTransformer


class Embedding:
    def __init__(self, parent):
        self.parent = parent
        self.start()
    
    def start(self):
        model_en = SentenceTransformer('all-MiniLM-L6-v2')
        sentences = self.parent.gui.label_3.text()
        print(sentences)
        embeddings = model_en.encode(sentences)
        print(embeddings)