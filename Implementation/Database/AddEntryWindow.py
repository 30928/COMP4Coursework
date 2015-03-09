from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
import re

class dbAddEntryWindow(QDialog):
    """add entry window dialog"""

    def __init__(self):
        super().__init__()

    def initAddEntryWindow(self):
        self.setWindowTitle("Add Entry")
        self.setFixedSize(640,115)
        self.setModal(True) #modal window
        self.AddEntryTable = QTableWidget(self) #table for adding customer entry
        self.AddEntryTable.setRowCount(1)
        self.AddEntryTable.setColumnCount(6)
        self.AddEntryTable.setFixedSize(617, 55)
        self.inputList = []
        for count in range(0, 6):
            #0 firstname, 1 lastname, 2 email, 3 phoneno, 4 address, 5 postcode 
            self.input = QLineEdit(self)
            self.input.setFrame(False)
            self.inputList.append(self.input)
            self.AddEntryTable.setCellWidget(0, count, self.input)
        
        self.inputList[0].setValidator(QRegExpValidator(QRegExp("[a-zA-Z\-\!]+")))
        self.inputList[1].setValidator(QRegExpValidator(QRegExp("[a-zA-Z\-\!]+")))
        self.inputList[2].setValidator(QRegExpValidator(QRegExp("^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")))
        self.regexp = "^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|"
        self.regexp2 = "((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$"
        self.inputList[3].setValidator(QRegExpValidator(QRegExp("{}{}".format(self.regexp, self.regexp2))))
        self.inputList[4].setValidator(QRegExpValidator(QRegExp("[a-zA-Z \d\-\.]+")))
        self.inputList[5].setValidator(QRegExpValidator(QRegExp("^[a-zA-Z]{1,2}[0-9][0-9A-Za-z]{0,1} {0,1}[0-9][A-Za-z]{2}$")))
        #2, 3 & 5 from www.regexlib.com
        self.CustomerHeaders = ["Firstname", "Lastname", "Email", "Phonenumber", "Address", "Postcode"]
        self.AddEntryTable.setHorizontalHeaderLabels(self.CustomerHeaders)
        self.btnConfirm = QPushButton("Confirm", self) #buttons
        self.btnCancel = QPushButton("Cancel", self)
        self.horizontal = QHBoxLayout()
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnCancel)
        self.horizontal.addWidget(self.btnConfirm)
        
        self.vertical = QVBoxLayout() #vbox layout
        self.vertical.addWidget(self.AddEntryTable)
        self.vertical.addStretch(1)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        
        self.btnCancel.clicked.connect(self.reject) #reject on clicking cancel
        self.btnConfirm.clicked.connect(self.AddEntryTodb) #call function after clicking confirm
        self.exec_()

    def AddEntryTodb(self):
        #fetching inputs from table
        self.Valid = True
        self.Message = "All Fields must be filled."
        self.Firstname = self.inputList[0].text()
        self.Lastname = self.inputList[1].text()
        self.Email = self.inputList[2].text()
        self.Phonenumber = self.inputList[3].text()
        self.Address = self.inputList[4].text()
        self.Postcode = self.inputList[5].text()
        
        self.input_data = (self.Firstname, self.Lastname, self.Email, self.Phonenumber, self.Address, self.Postcode)
        for count in range(0, len(list(self.input_data))):
            if list(self.input_data)[count].replace(" ", "") == "":
                self.Valid = False
        try:
            float(self.input_data[4])
            self.Valid = False
            self.Message = "Invalid Address"
        except:
            pass
        
        if self.Valid == True:
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                sql = "insert into Customer (FirstName, LastName, Email, PhoneNumber, Address, Postcode) values (?, ?, ?, ?, ?, ?)"
                cursor.execute(sql, self.input_data)
                db.commit()
                self.accept()
        else:
            self.Msg = QMessageBox()
            self.Msg.setWindowTitle("Invalid Entry")
            self.Msg.setText(self.Message)
            self.Msg.exec_()
