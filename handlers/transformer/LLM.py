from PyQt5.QtCore import QThread, pyqtSignal
import ollama

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
            prompt = f"""Определи дубликат или похожий по смыслу рационализаторское предложение.

                НОВОЕ: {self.new_name}
                СУЩЕСТВУЮЩЕЕ: {self.best_name}
                СХОДСТВО: {self.max_similarity:.2f}

                ОТВЕТЬ ТОЛЬКО 4 СТРОК:
                СХОДСТВО: [одна фраза, укажи существующее название]
                РАЗЛИЧИЯ: [одна фраза]  
                ДУБЛИКАТ: [ДА/НЕТ]
                РЕКОМЕНДАЦИЯ: [ДОБАВИТЬ/НЕ ДОБАВЛЯТЬ]"""

            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": 0.1,     
                    "num_predict": 250,     
                    "num_batch": 1024, 
                }
            )
                
            self.LLM_analys_finished.emit(response["message"]["content"])
        
        except Exception as e:
            self.LLM_analys_error.emit(f"Error - {e}")