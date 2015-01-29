from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbRoyaltiesAndInvoices(QDialog):
    """viewing royalties and invoices"""

    def __init__(self):
        super().__init__()

    def PubInvoice(self):
        self.setWindowTitle("View Publishing Invoices")
        self.setModal(True)
        self.setFixedSize(640, 220)
        self.vertical = QVBoxLayout(self)
        self.vertical.addWidget(self.table)
        self.btnAddPubInvoice.setFixedSize(100, 40)
        self.btnUpdatePubInvoice.setFixedSize(100, 40)
        self.btnDeleteEntry.setFixedSize(100, 40)
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.btnAddPubInvoice)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnUpdatePubInvoice)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnDeleteEntry)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        
        self.exec_()
        
    def PubInvoiceButtons(self):
        self.btnAddPubInvoice = QPushButton("Add Publishing \n Invoice", self)
        self.btnUpdatePubInvoice = QPushButton("Update Publishing \n Invoice", self)
        self.btnDeleteEntry = QPushButton("Delete \n Entry", self)        


    def BookInvoice(self):
        self.setWindowTitle("View Book Invoices")
        self.setModal(True)
        self.setFixedSize(640, 220)
        self.vertical = QVBoxLayout(self)
        self.vertical.addWidget(self.table)
        self.btnViewBookInvoiceItems.setFixedSize(100, 40)
        self.btnAddBookInvoice.setFixedSize(100, 40)
        self.btnUpdateBookInvoice.setFixedSize(100, 40)
        self.btnDeleteEntry.setFixedSize(100, 40)
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.btnViewBookInvoiceItems)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnAddBookInvoice)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnUpdateBookInvoice)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnDeleteEntry)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        
        self.exec_()
        
    def BookInvoiceButtons(self):
        self.btnViewBookInvoiceItems = QPushButton("View Book \n Invoice Items", self) 
        self.btnAddBookInvoice = QPushButton("Add Book \n Invoice", self)
        self.btnUpdateBookInvoice = QPushButton("Update Book \n Invoice", self)
        self.btnDeleteEntry = QPushButton("Delete \n Entry", self)
        
    def Royalties(self):
        self.setWindowTitle("View Royalties")
        self.setModal(True)
        self.setFixedSize(640, 220)
        self.vertical = QVBoxLayout(self)
        self.vertical.addWidget(self.table)
        self.btnViewRoyaltyItems.setFixedSize(100, 40)
        self.btnAddRoyalties.setFixedSize(100, 40)
        self.btnUpdateRoyalties.setFixedSize(100, 40)
        self.btnDeleteEntry.setFixedSize(100, 40)
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.btnViewRoyaltyItems)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnAddRoyalties)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnUpdateRoyalties)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnDeleteEntry)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        
        self.exec_()
        
    def RoyaltiesButtons(self):
        self.btnViewRoyaltyItems = QPushButton("View Royalty \n Items", self) 
        self.btnAddRoyalties = QPushButton("Add \n Royalties", self)
        self.btnUpdateRoyalties = QPushButton("Update \n Royalties", self)
        self.btnDeleteEntry = QPushButton("Delete \n Entry", self)        

