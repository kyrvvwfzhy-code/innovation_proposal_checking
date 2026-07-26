from PyQt5.QtWidgets import QMessageBox  

def info_message(parent, message):
    QMessageBox.information(parent, "Успех", message)
    
def critical_message(parent, message):
    QMessageBox.critical(parent, "Ошибка", message)

def question_message(parent, message, value):
    reply = QMessageBox.question(parent,
            "Подтверждение уникальности",
            f"{message}\"{value}\"?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
    if reply == QMessageBox.No:
        return False

def delete_question_message(parent, message, value):
    reply = QMessageBox.question(parent,
        "Подтверждение удаления",
        f"{message}\"{value}\"?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
        )
        
    if reply == QMessageBox.Yes:
        return True