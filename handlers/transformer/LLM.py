from PyQt5.QtCore import QThread, pyqtSignal
import ollama

from data.data import base_prompt_text

class LLM_analys_Thread(QThread):
    LLM_analys_finished = pyqtSignal(str)
    LLM_analys_error = pyqtSignal(str)
    
    def __init__(self, max_similarity, best_name, new_name):
        super().__init__()
        self.max_similarity = max_similarity
        self.best_name = best_name
        self.new_name = new_name

    def run(self):
        try:
            model = "bambucha/saiga-llama3"
            prompt = base_prompt_text(self.new_name, self.best_name, self.max_similarity)

            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": 0.1,     
                    "num_predict": 150,     
                    "num_batch": 2048, 
                }
            )
                
            self.LLM_analys_finished.emit(response["message"]["content"])
        
        except Exception as e:
            self.LLM_analys_error.emit(f"Error - {e}")