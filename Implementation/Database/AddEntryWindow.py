from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbAddEntryWindow(QDialog):
    """add entry window dialog"""

    def __init__(self):
        super().__init__()

    def initAddEntryWindow(self):
        self.setWindowTitle("Add Entry")
        self.setFixedSize(617,90)
        self.setModal(True) #modal window
        self.AddEntryTable = QTableWidget(self) #table for adding customer entry
        self.AddEntryTable.setRowCount(1)
        self.AddEntryTable.setColumnCount(6)
        self.AddEntryTable.setFixedSize(617, 55)
        self.CustomerHeaders = ["Firstname", "Lastname", "Email", "Phonenumber", "Address", "Postcode"]
        self.AddEntryTable.setHorizontalHeaderLabels(self.CustomerHeaders)
        self.label = QLabel("123123123", self)
        self.label.move(60,60)
        self.btnConfirm = QPushButton("Confirm", self) #buttons
        self.btnCancel = QPushButton("Cancel", self)
        self.btnConfirm.move(530, 60)
        self.btnCancel.move(450, 60)
        
        self.vertical = QVBoxLayout() #vbox layout        
        self.vertical.addWidget(self.AddEntryTable)

        self.btnConfirm.clicked.connect(self.accept) #accept on clicking confirm
        self.btnCancel.clicked.connect(self.reject) #reject on clicking cancel
        self.btnConfirm.clicked.connect(self.AddEntryTodb) #call function after clicking confirm
        self.exec_()

    def initAddBookWindow(self):
        self.setWindowTitle("Add Book")
        self.setFixedSize(700,280)
        self.setModal(True) #modal window

        self.btnDate = QPushButton("Date", self) #buttons,line edits and combo boxes
        self.qleDate = QLineEdit(self)
        self.cbAuthorID = QComboBox(self)
        self.qleBookTitle = QLineEdit(self)
        self.qleBookTitle.setPlaceholderText("Insert Book Title")
        self.qleNoOfPages = QLineEdit(self)
        self.cbSize = QComboBox(self)
        self.cbBack = QComboBox(self)
        self.qleISBN = QLineEdit(self)
        self.qleFont = QLineEdit(self)
        self.qleFontSize = QLineEdit(self)
        self.cbCover = QComboBox(self)
        self.qlePrice = QLineEdit(self)
        self.cbPaper = QComboBox(self)
        self.btnAddTodb = QPushButton("Add To Database", self)
        self.btnCancel = QPushButton("Cancel", self)

        self.horizontalTop = QHBoxLayout()
        self.horizontalTop.addWidget(self.btnDate)
        self.horizontalTop.addWidget(self.qleDate)
        
        self.verticalLeft = QVBoxLayout() #left side
        self.verticalLeft.addLayout(self.horizontalTop)
        self.verticalLeft.addWidget(self.cbAuthorID)
        self.verticalLeft.addWidget(self.qleBookTitle)
        self.verticalLeft.addWidget(self.qleNoOfPages)
        self.verticalLeft.addWidget(self.cbSize)
        self.verticalLeft.addWidget(self.cbBack)
        self.verticalLeft.addWidget(self.qleISBN)
        self.verticalLeft.addWidget(self.qleFont)

        self.horizontalBottom = QHBoxLayout()
        self.horizontalBottom.addWidget(self.btnCancel)
        self.horizontalBottom.addWidget(self.btnAddTodb)
        
        self.verticalRight = QVBoxLayout() #right side
        self.verticalRight.addWidget(self.cbCover)
        self.verticalRight.addWidget(self.qlePrice)
        self.verticalRight.addWidget(self.qleFontSize)
        self.verticalRight.addWidget(self.cbPaper)
        self.verticalRight.addStretch(1)
        self.verticalRight.addLayout(self.horizontalBottom)

        self.mainHorizontal = QHBoxLayout()
        self.mainHorizontal.addLayout(self.verticalLeft)
        self.mainHorizontal.addLayout(self.verticalRight)
        self.setLayout(self.mainHorizontal)
        
        self.btnAddTodb.clicked.connect(self.accept) #accept on clicking confirm
        self.btnCancel.clicked.connect(self.reject) #reject on clicking cancel
        
        self.exec_()        
    
    def AddEntryTodb(self):
        #fetching inputs from table
        self.Firstname = QTableWidgetItem(self.AddEntryTable.item(0, 0)).text()
        self.Lastname = QTableWidgetItem(self.AddEntryTable.item(0, 1)).text()
        self.Email = QTableWidgetItem(self.AddEntryTable.item(0, 2)).text()
        self.Phonenumber = QTableWidgetItem(self.AddEntryTable.item(0, 3)).text()
        self.Address = QTableWidgetItem(self.AddEntryTable.item(0, 4)).text()
        self.Postcode = QTableWidgetItem(self.AddEntryTable.item(0, 5)).text()
        
        self.input_data = (self.Firstname, self.Lastname, self.Email, self.Phonenumber, self.Address, self.Postcode)
        
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")
            sql = "insert into Customer (FirstName, LastName, Email, PhoneNumber, Address, Postcode) values (?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, self.input_data)
            db.commit()
