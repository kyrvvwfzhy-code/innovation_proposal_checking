from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import subprocess
from db.database import DataBase


class Loaded_documents:
    def __init__(self, parent):
        self.parent = parent
        self.db = DataBase()
        self.init()
    
    def init(self):
        self.create_table()
    
    def create_table(self):
        self.table = QTableWidget(self.parent)
        self.table_setup()
        data = self.db.get_key_information()
        if data:
            self.add_data(data)
        else:
            pass

        self.table.cellDoubleClicked.connect(self.open_file)
        self.parent.gui.pushButton.clicked.connect(self.delete_file)

    def table_setup(self):
        self.table.setGeometry(QtCore.QRect(10, 70, 1180,550))
        headers = ["№", "Имя файла", "Номер регистрации", "Дата Регистрации", "Наименование", "Автор"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 25)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        header = self.table.horizontalHeader()
        for i in range(1, self.table.columnCount()):  
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
        subprocess.call(['xdg-open', file_path[0]])
    
    def delete_file(self, row):
        filename = self.table.item(row, 1)
        if row >= 0:
            reply = QMessageBox.question(
                self.parent,
                "Подтверждение удаления",
                "Вы уверены, что хотите удалить эту запись?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.db.delete_ip(filename.text())
                self.table.removeRow(row)
                self.update_row_numbers()
    
    def update_row_numbers(self):
        for row in range(self.table.rowCount()):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        
        


        
        