from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class TableWidget(QMainWindow):
    """table widget"""

    def __init__(self):
        super().__init__()
        
    def initTable(self):
        self.table = QTableWidget()
        self.table.setFixedSize(716,275)
        
    def CustomerTable(self):
        self.table.clear()
        self.table.setColumnCount(7)
        self.table.setRowCount(1)
        
        CustomerHeaders = ["AuthorID", "Forename", "Surname", "Email", "Phonenumber", "Address", "Postcode"]
        self.table.setHorizontalHeaderLabels(CustomerHeaders)

        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")
            
            sql = "select all AuthorID from Customer"
            cursor.execute(sql)
            self.AuthorIDList = list(cursor.fetchall())

            sql = "select all Firstname from Customer"
            cursor.execute(sql)
            self.FirstnameList = list(cursor.fetchall())

            sql = "select all Lastname from Customer"
            cursor.execute(sql)
            self.LastnameList = list(cursor.fetchall())

            sql = "select all Email from Customer"
            cursor.execute(sql)
            self.EmailList = list(cursor.fetchall())
            
            sql = "select all Phonenumber from Customer"
            cursor.execute(sql)
            self.PhonenumberList = list(cursor.fetchall())

            sql = "select all Address from Customer"
            cursor.execute(sql)
            self.AddressList = list(cursor.fetchall())

            sql = "select all Postcode from Customer"
            cursor.execute(sql)
            self.PostcodeList = list(cursor.fetchall())


        
        for count in range(0, len(self.AuthorIDList)):
            self.table.insertRow(1)
            AuthorID = self.AuthorIDList[count]
            AuthorID = list(AuthorID)[0]
            self.table.setItem(count, 0, QTableWidgetItem(str(AuthorID)))

            Firstname = self.FirstnameList[count]
            Firstname = list(Firstname)[0]
            self.table.setItem(count, 1, QTableWidgetItem(str(Firstname)))
            
            Lastname = self.LastnameList[count]
            Lastname = list(Lastname)[0]
            self.table.setItem(count, 2, QTableWidgetItem(str(Lastname)))

            Email = self.EmailList[count]
            Email = list(Email)[0]
            self.table.setItem(count, 3, QTableWidgetItem(str(Email)))

            Phonenumber = self.PhonenumberList[count]
            Phonenumber = list(Phonenumber)[0]
            self.table.setItem(count, 4, QTableWidgetItem(str(Phonenumber)))

            Address = self.AddressList[count]
            Address = list(Address)[0]
            self.table.setItem(count, 5, QTableWidgetItem(str(Address)))

            Postcode = self.PostcodeList[count]
            Postcode = list(Postcode)[0]
            self.table.setItem(count, 6, QTableWidgetItem(str(Postcode)))

    def AddEntryToTable(self, addEntryDlg):
        self.initTable(self)
        self.CustomerTable(self)
        self.table.insertRow(1)
        for count in range(1, 6):
            self.table.setItem(1, count, QTableWidgetItem(str(addEntryDlg.EntryList[count])))

   

    

            

