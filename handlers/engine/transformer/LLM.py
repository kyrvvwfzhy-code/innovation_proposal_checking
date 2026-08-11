from PyQt5.QtCore import QThread, pyqtSignal

import ollama

from data.data import base_prompt_text

class LLM_analys_Thread(QThread):
    LLM_analys_finished = pyqtSignal(list)
    LLM_analys_error = pyqtSignal(str)
    
    def __init__(self, result, new_name):
        super().__init__()
        self.result = result
        self.new_name = new_name

    def run(self):
        try:
            model = "qwen2.5:7b"
            response_text, prompt = base_prompt_text(self.result, self.new_name)

            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": 0.1,     
                    "num_predict": 300,
                    "repeat_penalty": 1.1,
                    "num_batch": 2048, 
                }
            )
            
            result = [response_text, response["message"]["content"], [self.new_name]]
            self.LLM_analys_finished.emit(result)
        
        except Exception as e:
            self.LLM_analys_error.emit(f"Error - {e}")