from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys


class dbSearchDatabase(QDialog):
    """initialising the detailed search window"""

    def __init__(self):
        super().__init__()
        
    def initLayout(self):
        self.gridLayout = QGridLayout()
        self.setFixedSize(400, 200)
        self.leFirstname = QLineEdit(self)
        self.leLastname = QLineEdit(self)
        self.cbTable = QComboBox(self)
        self.cbCategory = QComboBox(self)
        self.btnDate = QPushButton("Add Date", self)
        self.leSearch = QLineEdit(self)
        self.btnCancel = QPushButton("Cancel", self)
        self.btnSearch = QPushButton("Search", self)
        self.btnDate.setFixedSize(60, 25)
        self.lblFirstname = QLabel("Author Firstname:")
        self.lblLastname = QLabel("Author Lastname:")
        self.gridLayout.addWidget(self.leFirstname, 0, 3)
        self.gridLayout.addWidget(self.leLastname, 1, 3)
        self.gridLayout.addWidget(self.lblFirstname, 0, 2, Qt.AlignRight)
        self.gridLayout.addWidget(self.lblLastname, 1, 2, Qt.AlignRight)
        self.gridLayout.addWidget(self.cbTable, 0, 0)
        self.gridLayout.addWidget(self.cbCategory, 2, 0)
        self.gridLayout.addWidget(self.btnDate, 2, 1, Qt.AlignHCenter)
        self.gridLayout.addWidget(self.leSearch, 2, 2, 1, 2)
        self.gridLayout.addWidget(self.btnCancel, 3, 2)
        self.gridLayout.addWidget(self.btnSearch, 3, 3)
        self.setLayout(self.gridLayout)
        self.cbTable.addItem("Author")
        self.cbTable.addItem("Book")
        self.cbTable.addItem("Publishing Invoice")
        self.cbTable.addItem("Book Invoice")
        self.cbTable.addItem("Book Invoice Items")
        self.cbTable.addItem("Royalties")
        self.cbTable.addItem("Royalty Items")
        self.cbTable.activated[str].connect(self.ChangeCategories)
        self.exec_()
        
    def ChangeCategories(self):
        if self.cbTable.currentText() == "Customer":
            pass
        elif self.cbTable.currentText() == "Book":
            pass
        elif self.cbTable.currentText() == "PubInvoice":
            pass
        elif self.cbTable.currentText() == "BookInvoice":
            pass
        elif self.cbTable.currentText() == "BookInvoiceItems":
            pass
        elif self.cbTable.currentText() == "Royalties":
            pass
        elif self.cbTable.currentText() == "RoyaltyItems":
            pass
