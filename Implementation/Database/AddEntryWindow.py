from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbAddEntryWindow(QDialog):
    """add entry window dialog"""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""QTableWidget{
                                        gridline-color: #A8A800;
                                        border-color: #A8A800;
                                        selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5,
                                        stop: 0 #A8A800, stop: 1 #8F8F00 )}
                            QPushButton{
                                min-height: 2em;
                                min-width: 5em;
                                border-style: outset;
                                border-width: 1px;
                                border-color: #8F8F00;
                                color: black;
                                background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5,
                                stop: 0 #E8E85D, stop: 1 white);
                                padding: 1px;}
                            QPushButton:pressed {
                                background-color: lightgray}
                            
                            }""")

    def initAddEntryWindow(self):
        self.setWindowTitle("Add Entry")
        self.setFixedSize(640,115)
        self.setModal(True) #modal window
        self.AddEntryTable = QTableWidget(self) #table for adding customer entry
        self.AddEntryTable.setRowCount(1)
        self.AddEntryTable.setColumnCount(6)
        self.AddEntryTable.setFixedSize(617, 55)
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
        self.Firstname = QTableWidgetItem(self.AddEntryTable.item(0, 0)).text()
        self.Lastname = QTableWidgetItem(self.AddEntryTable.item(0, 1)).text()
        self.Email = QTableWidgetItem(self.AddEntryTable.item(0, 2)).text()
        self.Phonenumber = QTableWidgetItem(self.AddEntryTable.item(0, 3)).text()
        self.Address = QTableWidgetItem(self.AddEntryTable.item(0, 4)).text()
        self.Postcode = QTableWidgetItem(self.AddEntryTable.item(0, 5)).text()
        
        self.input_data = (self.Firstname, self.Lastname, self.Email, self.Phonenumber, self.Address, self.Postcode)
        for count in range(0, len(list(self.input_data))):
            if list(self.input_data)[count].replace(" ", "") == "":
                self.Valid = False
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
            self.Msg.setText("All Fields must be filled.")
            self.Msg.exec_()
