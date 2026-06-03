from OCR.conversion_thread import Conversion_Thred
import os

class OCR_main:
    def __init__(self):
        self.thread = None
        self.start_ocr()
    
    
    def start_ocr(self):
            
        self.thread = Conversion_Thred()
        self.thread.signal.connect(self.on_message)
        self.thread.finished.connect(self.on_thread_finished)  # Сигнал завершения
        self.thread.start()
    
    def on_message(self, msg):
        print(msg)
    
    def on_thread_finished(self):
        print("Закончился")
        
 

if __name__ == "__main__":
    OCR_main()