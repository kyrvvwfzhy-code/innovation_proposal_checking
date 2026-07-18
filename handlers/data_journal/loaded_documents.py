from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore
import sys
import os
import subprocess
from data.messagebox import delete_question_message


class Loaded_documents:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.init()
    
    def init(self):
        self.create_table()
    
    def create_table(self):
        self.table = QTableWidget(self.parent)
        self.table_setup()
        data = self.db.get_key_information()
        if data:
            self.add_data(data)

        # self.table.cellDoubleClicked.connect(self.open_file)
        self.parent.gui.pushButton.clicked.connect(self.delete_selected)

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

    def add_data(self, data):
        self.table.setRowCount(len(data))
        for row, record in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            for col, value in enumerate(record, start=1):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
    
    def open_file(self, row):
        filename = self.table.item(row, 1)
        file_path = self.db.get_loaded_ip(filename.text())
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
        
    def update_row_numbers(self):
        for row in range(self.table.rowCount()):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        
        


        
        