from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore
import sys
import os
import subprocess
from data.messagebox import delete_question_message
from data.messagebox import info_message, critical_message
from log.logging import logger
from handlers.engine.transformer.vectorization import Vectorization_Thread

class Journal_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.create_table()
    
    def create_table(self):
        self.table = QTableWidget(self.parent)
        self.table_setup()
        data = self.db.get_key_information()
        if data:
            self.add_data(data)

        self.table.itemDoubleClicked.connect(self.edit_item)

    def table_setup(self):
        self.table.setGeometry(QtCore.QRect(10, 80, 880,520))
        headers = ["№", "Имя файла", "Зарегестрирован", "Наименование"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 25)
        
        self.table.setWordWrap(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.setColumnWidth(1, 100)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        header = self.table.horizontalHeader()
        for i in range(2, self.table.columnCount()):  
            header.setSectionResizeMode(i, QHeaderView.Stretch)
    
    def edit_item(self, item):
        """Редактирование при двойном клике на любую ячейку"""
        row = item.row()
        col = item.column()
        
        if col == 0 or col == 1:
            self.open_file(row)
            return
        
        self.table.editItem(item)

    def add_data(self, data):
        self.table.setRowCount(len(data))
        for row, record in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            for col, value in enumerate(record, start=1):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
    
    def open_file(self, row):
        filename = self.table.item(row, 1).text()
        file_path = self.db.get_loaded_ip(filename)
        if sys.platform == 'win32':
            os.startfile(file_path[0])
        else:
            subprocess.call(['xdg-open', file_path[0]])
    
    def delete_selected(self):
        row = self.table.currentRow()
        
        if row < 0:
            QMessageBox.warning(self.parent, "Ошибка", "Выберите запись для удаления.", QMessageBox.Ok)
            return
        
        filename = self.table.item(row, 1).text()
        reply = delete_question_message(self.parent, "Удалить запись", filename)
        if reply == True:
            self.db.delete_ip(filename)
            self.db.delete_embeddings(filename)
            self.table.removeRow(row)
            self.update_row_numbers()
    
    def save_changes(self):
        try:
            saved_rows = 0
            unchanged_rows = 0
            
            for row in range(self.table.rowCount()):
                filename = self.table.item(row, 1).text()
                registration_date = self.table.item(row, 2).text()  
                name = self.table.item(row, 3).text()  
                
                result = self.db.update_key_information(filename, registration_date, name)
                
                if result > 0:
                    saved_rows += 1
                    self.vector_update(filename, name)
                    logger.info(f"Строка {row} обновлена: {filename}")
                else:
                    unchanged_rows += 1

            if saved_rows > 0:
                info_message(self.parent, f"Данные успешно сохранены! Обновлено {saved_rows} записей.")
            else:
                critical_message(self.parent, "Изменений не обнаружено.")
                
        except Exception as e:
            logger.error(f"Ошибка при сохранении: {e}")
            critical_message(self.parent, f"Ошибка при сохранении: {e}")
    
    def update_table(self, loaded_documents):
        if loaded_documents is not None:
                if hasattr(loaded_documents, 'table'):
                    loaded_documents.table.setRowCount(0)
                    data = self.db.get_key_information()
                    if data:
                        loaded_documents.add_data(data)
                    logger.info("✅ Таблица обновлена")
                    return
    
    def vector_update(self, filename, name):
        self.thread = Vectorization_Thread(self.parent, name)
        self.thread.vectorization_finished.connect(
        lambda new_embedding: self.vectorization_finished(new_embedding, filename)
        )
        self.thread.vectorization_error.connect(self.vectorization_error)
        self.thread.start()
    
    def vectorization_finished(self, new_embedding, filename):
        self.db.update_embedding(filename, new_embedding)
        
        logger.info(f"Эмбеддинг файла {filename} обновился в связи с изменениями в журнале")
            
    def vectorization_error(self, error):
        logger.error(f"ОШИБКА - Эмбеддинг файла не обновился. {error}")
        self.thread.deleteLater()
        
    def update_row_numbers(self):
        for row in range(self.table.rowCount()):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
    
    
        
        
        


        
        