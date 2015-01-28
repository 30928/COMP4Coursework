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
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        with sqlite3.connect("PP.db") as db: #fetching data from db
            cursor = db.cursor()
            cursor.execute(self.sql)
        self.columns = [tuple[0] for tuple in cursor.description]
        self.setRowCount(0)
        self.setColumnCount(len(self.columns))
        self.setHorizontalHeaderLabels(self.columns)
        for self.row, form in enumerate(cursor):
            self.insertRow(self.row)
            for self.column, item in enumerate(form):
                self.setItem(self.row, self.column, QTableWidgetItem(str(item)))
