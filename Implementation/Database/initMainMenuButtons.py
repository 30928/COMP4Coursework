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
        
        self.btnLogOut = QPushButton("Log Out", self)
        self.btnLogOut.setFixedSize(100, 30)
        
        self.leQuickSearch = QLineEdit(self)
        self.leQuickSearch.setPlaceholderText("Author Name")
        self.leQuickSearch.setFixedSize(100, 25)
        
        self.btnQuickSearch = QPushButton("Quick Search", self)
        self.btnQuickSearch.setFixedSize(100, 30)

        self.horizontalTop = QHBoxLayout()
        self.horizontalTop.addWidget(self.btnLogOut)
        self.horizontalTop.addStretch(1)
        self.horizontalTop.addWidget(self.leQuickSearch)
        self.horizontalTop.addWidget(self.btnQuickSearch)

        self.btnView = QPushButton("View", self)
        self.btnView.setFixedSize(100, 40)
        
        self.btnSearchdb = QPushButton("Search Database", self)
        self.btnSearchdb.setFixedSize(100, 40)
        
        self.btnAddEntry = QPushButton("Add Entry", self)
        self.btnAddEntry.setFixedSize(100, 40)
        
        self.btnUpdateEntry = QPushButton("Update Entry", self)
        self.btnUpdateEntry.setFixedSize(100, 40)
        
        self.btnRemoveEntry = QPushButton("Remove Entry", self)
        self.btnRemoveEntry.setFixedSize(100, 40)
        
        self.btnChangePassword = QPushButton("Change Username/\nPassword", self)
        self.btnChangePassword.setFixedSize(100, 40)
    
        self.horizontalBottom = QHBoxLayout()
        
        self.horizontalBottom.addWidget(self.btnView)
        self.horizontalBottom.addWidget(self.btnSearchdb)
        self.horizontalBottom.addWidget(self.btnAddEntry)
        self.horizontalBottom.addWidget(self.btnUpdateEntry)
        self.horizontalBottom.addWidget(self.btnRemoveEntry)
        self.horizontalBottom.addWidget(self.btnChangePassword)
