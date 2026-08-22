from PyQt5.QtWidgets import QMessageBox  

#GENERAL
def info_message(parent, message):
    QMessageBox.information(parent, "Успех", message)
    
def critical_message(parent, message):
    QMessageBox.critical(parent, "Ошибка", message)

#DOWNLOAD
def conclusion_question(parent, message, value):
    reply = QMessageBox.question(parent,
            "Заключение",
            f"{message}\n\n\"{value}\"",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
            )
            
    if reply == QMessageBox.No:
        return False

#JOURNAL
def delete_question_message(parent, message, value):
    reply = QMessageBox.question(parent,
        "Подтверждение удаления",
        f"{message}\n\n{value}",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
        )
        
    if reply == QMessageBox.Yes:
        return True