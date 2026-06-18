from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
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
        print(data)
        if data:
            self.add_data(data)
        else:
            pass

    def table_setup(self):
        self.table.setGeometry(QtCore.QRect(10, 70, 1180,620))
        headers = ["№", "Имя файла", "Путь файла", "Номер регистрации", "Дата Регистрации", "Наименование", "Автор"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 25)
        header = self.table.horizontalHeader()
        for i in range(1, self.table.columnCount()):  
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def add_data(self, data):
        self.table.setRowCount(len(data))
        for row, record in enumerate(data):
            for col, value in enumerate(record):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
        
        
        


        
        