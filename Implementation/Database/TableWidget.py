from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class dbTableWidget(QTableWidget):
    """main table widget"""

    def __init__(self):
        super().__init__()
        self.setFixedSize(716,275)
        
    def CustomerTable(self):
        
        self.clear()
        self.setColumnCount(7)
        self.setRowCount(1)
        
        CustomerHeaders = ["AuthorID", "Forename", "Surname", "Email", "Phonenumber", "Address", "Postcode"]
        self.setHorizontalHeaderLabels(CustomerHeaders)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def initTable(self):
        self.clear()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        with sqlite3.connect("PP.db") as db: #fetching all data from db
            cursor = db.cursor()
            sql = "select * from {}".format(self.currentTable)
            cursor.execute(sql)
        self.columns = [tuple[0] for tuple in cursor.description]
        self.setHorizontalHeaderLabels(self.columns)
        self.setRowCount(0)

        for self.row, form in enumerate(cursor):
            self.insertRow(self.row)
            for self.column, item in enumerate(form):
                self.item = QTableWidgetItem(str(item))
                self.setItem(self.row, self.column, self.item) 
