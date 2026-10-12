from PyQt5.QtCore import QThread, pyqtSignal

from data.output_message import conclusion_AI_forming

class LLM_analys_Thread(QThread):
    LLM_analys_finished = pyqtSignal(list)
    LLM_analys_error = pyqtSignal(str)
    
    def __init__(self, db, result, new_name, instruct_model):
        super().__init__()
        self.db = db
        self.result = result
        self.new_name = new_name
        self.instruct_model = instruct_model

    def run(self):
        try:
            prompt_text = self.db.get_innovation_proposal_prompt()
            response_text, prompt = conclusion_AI_forming(prompt_text, self.result, self.new_name)

            response = self.instruct_model.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300,
                repeat_penalty=1.1
            )

            result = [response_text, response["choices"][0]["message"]["content"], [self.new_name]]
            self.LLM_analys_finished.emit(result)
        
        except Exception as e:
            self.LLM_analys_error.emit(f"Error - {e}")