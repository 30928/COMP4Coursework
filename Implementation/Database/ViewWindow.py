from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbViewWindow(QWidget):
    """generic view window"""

    def __init__(self):
        super().__init__()

    def View(self):
        self.setWindowTitle("View Menu")
        self.setFixedSize(735,400)

        self.btnBack = QPushButton("Back", self)
        self.btnBack.setFixedSize(100, 30)
        self.btnViewRoyalties = QPushButton("View Royalties", self)
        self.btnViewRoyalties.setFixedSize(100, 40)
        self.btnViewBookInvoices = QPushButton("View Book  \n Invoices", self)
        self.btnViewBookInvoices.setFixedSize(100, 40)
        self.btnViewPubInvoice = QPushButton("View Publishing \n Invoice", self)
        self.btnViewPubInvoice.setFixedSize(100, 40)
        self.btnAddBook = QPushButton("Add Book", self)
        self.btnAddBook.setFixedSize(100, 40)
        self.btnUpdateBook = QPushButton("Update Book", self)
        self.btnUpdateBook.setFixedSize(100,40)
        self.btnDeleteBook = QPushButton("Delete Book", self)
        self.btnDeleteBook.setFixedSize(100, 40)

        self.horizontalTop = QHBoxLayout()
        self.horizontalTop.addStretch(1)
        self.horizontalTop.addWidget(self.btnBack)

        self.horizontalBottom = QHBoxLayout()
        self.horizontalBottom.addWidget(self.btnViewPubInvoice)
        self.horizontalBottom.addWidget(self.btnViewBookInvoices)
        self.horizontalBottom.addWidget(self.btnViewRoyalties)
        self.horizontalBottom.addWidget(self.btnAddBook)
        self.horizontalBottom.addWidget(self.btnUpdateBook)
        self.horizontalBottom.addWidget(self.btnDeleteBook)

        self.vertical = QVBoxLayout()
