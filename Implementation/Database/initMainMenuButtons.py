from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys


class initMainMenuButtons(QWidget):
    """initialising the main menu buttons"""

    def __init__(self):
        super().__init__()
        

        #creating the layout
        
        self.vertical = QVBoxLayout()
        
        self.btnLogOut = QPushButton("Log Out")
        self.btnLogOut.setFixedSize(100,30)
        
        self.leQuickSearch = QLineEdit(QWidget(self))
        self.leQuickSearch.setPlaceholderText("Author Surname")
        self.leQuickSearch.setFixedSize(100,25)
        
        self.btnQuickSearch = QPushButton("Quick Search")
        self.btnQuickSearch.setFixedSize(100,30)

        self.horizontalTop = QHBoxLayout()
        self.horizontalTop.addWidget(self.btnLogOut)
        self.horizontalTop.addStretch(2)
        self.horizontalTop.addWidget(self.leQuickSearch)
        self.horizontalTop.addWidget(self.btnQuickSearch)
        
        self.vertical.addLayout(self.horizontalTop)
        #adding table widget
        self.table = QTableWidget() #creating main menu table
        self.table.setFixedSize(716,275)
        self.table.clear()
        self.table.setColumnCount(7)
        CustomerHeaders = ["AuthorID", "Firstname", "Lastname", "Email", "Phonenumber", "Address", "Postcode"]
        self.table.setHorizontalHeaderLabels(CustomerHeaders)
        self.vertical.addWidget(self.table)
        #self.initCustomers()
        #
        self.btnView = QPushButton("View")
        self.btnView.setFixedSize(100,40)
        
        self.btnSearchdb = QPushButton("Search Database")
        self.btnSearchdb.setFixedSize(100,40)
        
        self.btnAddEntry = QPushButton("Add Entry")
        self.btnAddEntry.setFixedSize(100,40)
        
        self.btnUpdateEntry = QPushButton("Update Entry")
        self.btnUpdateEntry.setFixedSize(100,40)
        
        self.btnRemoveEntry = QPushButton("Remove Entry")
        self.btnRemoveEntry.setFixedSize(100,40)
        
        self.btnChangePassword = QPushButton("Change Password")
        self.btnChangePassword.setFixedSize(100,40)
    
        self.horizontalBottom = QHBoxLayout()
        
        self.horizontalBottom.addWidget(self.btnView)
        self.horizontalBottom.addWidget(self.btnSearchdb)
        self.horizontalBottom.addWidget(self.btnAddEntry)
        self.horizontalBottom.addWidget(self.btnUpdateEntry)
        self.horizontalBottom.addWidget(self.btnRemoveEntry)
        self.horizontalBottom.addWidget(self.btnChangePassword)

        
        #self.buttons_widget = QWidget(self)
        self.vertical.addLayout(self.horizontalBottom)
        self.setLayout(self.vertical)
        #self.setCentralWidget(self.buttons_widget)
        
        self.btnAddEntry.clicked.connect(AddEntryWindow) #connection for 'add entry'
