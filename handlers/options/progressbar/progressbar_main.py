from handlers.options.progressbar.progressbar_logic import Progressbar_logic

class Progressbar:
    def __init__(self, parent, target):
        self.parent = parent
        self.target = target
        self.logic = Progressbar_logic(self.parent, self.target)
        self.logic.progress_update.connect(lambda : self.logic.deleteLater)
        self.logic.progress_error.connect(lambda : self.logic.deleteLater)
        self.logic.start()
