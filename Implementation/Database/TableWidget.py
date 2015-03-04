from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class dbTableWidget(QTableWidget):
    """main table widget"""

    def __init__(self):
        super().__init__()


    def initTable(self):
        self.clear()
        self.columns = []
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSortingEnabled(False)
        with sqlite3.connect("PP.db") as db: #fetching data from db
            cursor = db.cursor()
            cursor.execute(self.sql)
            self.ColumnNames = cursor.description
        for count in range(0, len(self.ColumnNames)):
            self.columns.append(list(list(self.ColumnNames)[count])[0])
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        for self.row, self.form in enumerate(cursor):
            self.insertRow(self.row)
            for self.column, self.unit in enumerate(self.form):
                self.setItem(self.row, self.column, QTableWidgetItem(str(self.unit)))
        self.setSortingEnabled(True)
