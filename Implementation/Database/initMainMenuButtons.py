from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
from AddEntryWindow import *
class initMainMenuButtons(QMainWindow):
    """initialising the main menu buttons"""

    def __init__(self):
        super().__init__()
        
    def Buttons(self):

        #creating the layout
        
        self.vertical = QVBoxLayout()
        
        self.btnLogOut = QPushButton("Log Out", QWidget(self))
        self.btnLogOut.setFixedSize(100,30)
        
        self.leQuickSearch = QLineEdit(QWidget(self))
        self.leQuickSearch.setPlaceholderText("Author Surname")
        self.leQuickSearch.setFixedSize(100,25)
        
        self.btnQuickSearch = QPushButton("Quick Search", QWidget(self))
        self.btnQuickSearch.setFixedSize(100,30)

        self.horizontalTop = QHBoxLayout()
        self.horizontalTop.addWidget(self.btnLogOut)
        self.horizontalTop.addStretch(2)
        self.horizontalTop.addWidget(self.leQuickSearch)
        self.horizontalTop.addWidget(self.btnQuickSearch)

        self.vertical.addLayout(self.horizontalTop)
        
        self.initTable()

        self.btnView = QPushButton("View", self)
        self.btnView.setFixedSize(100,40)
        
        self.btnSearchdb = QPushButton("Search Database", self)
        self.btnSearchdb.setFixedSize(100,40)
        
        self.btnAddEntry = QPushButton("Add Entry", self)
        self.btnAddEntry.setFixedSize(100,40)
        
        self.btnUpdateEntry = QPushButton("Update Entry", self)
        self.btnUpdateEntry.setFixedSize(100,40)
        
        self.btnRemoveEntry = QPushButton("Remove Entry", self)
        self.btnRemoveEntry.setFixedSize(100,40)
        
        self.btnChangePassword = QPushButton("Change Password", self)
        self.btnChangePassword.setFixedSize(100,40)
    
        self.horizontalBottom = QHBoxLayout()
        
        self.horizontalBottom.addWidget(self.btnView)
        self.horizontalBottom.addWidget(self.btnSearchdb)
        self.horizontalBottom.addWidget(self.btnAddEntry)
        self.horizontalBottom.addWidget(self.btnUpdateEntry)
        self.horizontalBottom.addWidget(self.btnRemoveEntry)
        self.horizontalBottom.addWidget(self.btnChangePassword)

        
        self.buttons_widget = QWidget()
        self.vertical.addLayout(self.horizontalBottom)
        self.buttons_widget.setLayout(self.vertical)
        self.setCentralWidget(self.buttons_widget)
        
        self.btnAddEntry.clicked.connect(AddEntryWindow) #connection for 'add entry'
        #AddEntryWindow.closeEvent.connect(self.RefreshTable)
