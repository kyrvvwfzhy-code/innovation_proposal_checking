from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore

from handlers.engine.Semantic_Search.vectorization import Vectorization_Thread

from data.messagebox import delete_question_message, info_message, critical_message

from log.logging import logger
import sys
import os
import subprocess

class Journal_logic:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.all_data = None
        self.thread = None
        self.create_table()
    
    def create_table(self):
        self.table = QTableWidget(self.parent)
        self.table_setup()

        self.all_data = self.db.get_innovation_proposal_info()
        if self.all_data:
            self.add_record(self.all_data)
            
#Настройки таблицы
    def table_setup(self):
        self.table.setGeometry(QtCore.QRect(20, 80, 860,520))
        headers = ["№", "Имя файла", "Зарегестрирован", "Наименование"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 30)
        
        self.table.setWordWrap(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.setColumnWidth(1, 100)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        header = self.table.horizontalHeader()
        for i in range(2, self.table.columnCount()):  
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        self.table.itemDoubleClicked.connect(self.edit_item)

#Добавление записей
    def add_record(self, data):
        self.table.setRowCount(len(data))
        for row, record in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            for col, value in enumerate(record, start=1):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

#Открытие файлов
    def edit_item(self, item):
        row = item.row()
        col = item.column()
        
        if col == 0 or col == 1:
            self.open_file(row)
            return
        
        self.table.editItem(item)

    def open_file(self, row):
        filename = self.table.item(row, 1).text()
        file_path = self.db.get_filepath_from_innovation_proposal(filename)
        if sys.platform == 'win32':
            os.startfile(file_path[0])
        else:
            subprocess.call(['xdg-open', file_path[0]])
        logger.info(f"JOURNAL | OPEN - {filename}")

#Удаление записей
    def delete_selected_records(self):
        selected_rows = sorted(set(item.row() for item in self.table.selectedItems()), reverse=True)
        
        if not selected_rows:
            logger.error(f"JOURNAL | FILE - nothing selected to delete")
            QMessageBox.warning(self.parent, "Ошибка", "Выберите записи для удаления.", QMessageBox.Ok)
            return
        
        filenames = [self.table.item(row, 1).text() for row in selected_rows]
        
        if len(filenames) == 1:
            msg = f"Удалить запись?"
            value = filenames[0]
        else:
            msg = f"Удалить следующие записи?"
            value = f"\n".join(filenames[:5])
            if len(filenames) > 5:
                msg += f"\n..."
                value += f" и ещё {len(filenames) - 5}"
        reply = delete_question_message(self.parent, msg, value)
        
        if reply == True:
            for row in sorted(selected_rows, reverse=True):
                filename = self.table.item(row, 1).text()
                self.db.delete_innovation_proposal(filename)
                self.table.removeRow(row)
                logger.info(f"JOURNAL | FILE - \"{filename}\" delete")
            
            self.update_row_numbers()
            self.all_data = self.db.get_innovation_proposal_info()

#Сохранение изменений   
    def save_changes(self):
        try:
            saved_rows = 0
            unchanged_rows = 0
            edit_data = []

            for row in range(self.table.rowCount()):
                filename = self.table.item(row, 1).text()
                registration_date = self.table.item(row, 2).text()  
                name = self.table.item(row, 3).text()  
                
                result = self.db.update_innovation_proposal_info(filename, registration_date, name)
                
                if result > 0:
                    saved_rows += 1
                    general_edit = filename, name
                    edit_data.append(general_edit)
                    logger.info(f"JOURNAL | UPDATE - {row} : {filename}")
                else:
                    unchanged_rows += 1

            if edit_data and saved_rows > 0:
                self.vector_update(edit_data)
                logger.info(f"JOURNAL | UPDATE - {saved_rows} rows")
                info_message(self.parent, f"Данные успешно сохранены! Обновлено {saved_rows} записей.")
                self.all_data = self.db.get_innovation_proposal_info()
            else:
                logger.error(f"JOURNAL | NOT UPDATE raws")
                critical_message(self.parent, "Изменений не обнаружено.")

        except Exception as e:
            logger.info(f"JOURNAL | NOT SAVE - {e}")
            critical_message(self.parent, f"Ошибка при сохранении: {e}")

    def vector_update(self, new_data):
        self.filenames = []
        names = []
        for i in new_data:
            self.filenames.append(i[0])
            names.append(i[1])
        self.thread = Vectorization_Thread(self.parent, names, level = "vector_update")
        self.thread.vectorization_finished.connect(self.vectorization_finished)
        self.thread.vectorization_error.connect(self.vectorization_error)
        self.thread.start()

    def vectorization_finished(self, new_embeddings):
        try:
            for filename, embedding in zip(self.filenames, new_embeddings):
                self.db.update_innovation_proposal_embeddings(filename, embedding)
                logger.info(f"JOURNAL | UPDATE - {filename} embedding by journal edit")
        finally:
            if self.thread:
                self.thread.deleteLater()
                self.thread = None

    def vectorization_error(self, error):
        logger.error(f"JOURNAL | NOT UPDATE - embedding : {error}")
        logger.error(f"ОШИБКА - Эмбеддинг файла не обновился. {error}")
        self.thread.deleteLater()

#Обновление таблицы
    def update_table(self, loaded_documents):
        if loaded_documents is not None:
            if hasattr(loaded_documents, 'table'):
                loaded_documents.table.setRowCount(0)
                self.all_data = self.db.get_innovation_proposal_info()
                if self.all_data:
                    loaded_documents.add_record(self.all_data)
                    logger.info(f"JOURNAL | UPDATE - table")
                return
            
    def update_row_numbers(self):
        for row in range(self.table.rowCount()):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))

#Поиск
    def search_record(self):
        text_to_search = self.parent.gui.lineEdit.text().strip()
        
        if not text_to_search:
            self.show_all_records()
            logger.info("JOURNAL | empty value")
            return

        found_data = []
        for record in self.all_data:
            if any(text_to_search.lower() in str(field).lower() for field in record):
                found_data.append(record)
        
        self.table.setRowCount(0)
        
        if found_data:
            self.add_record(found_data)
        else:
            logger.info(f"JOURNAL | NOT FOUND - {text_to_search}")
            critical_message(self.parent, f"По запросу '{text_to_search}' ничего не найдено")
            self.show_all_records()
    
    def show_all_records(self):
        self.table.setRowCount(0)
        if self.all_data:
            self.add_record(self.all_data)
    
    def reset_search(self):
        self.parent.gui.lineEdit.clear()
        self.show_all_records()
 