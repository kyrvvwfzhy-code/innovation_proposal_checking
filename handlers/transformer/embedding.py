# from sentence_transformers import SentenceTransformer


# class Embedding:
#     def __init__(self, parent):
#         self.parent = parent
#         self.start()
    
#     def start(self):
#         model_en = SentenceTransformer('all-MiniLM-L6-v2')
#         sentences = self.parent.gui.label_3.text()
#         print(sentences)
#         embeddings = model_en.encode(sentences)
#         self.parent.gui.plainTextEdit_2.setPlainText(embeddings)

class Embedding:
    def __init__(self, parent):
        self.parent = parent

    def start(self):
        text = self.process()
        self.parent.gui.plainTextEdit_2.setPlainText(text)
    def process(self,):
        result = "Подклюение LLM модели"
        return result 