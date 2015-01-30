from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbItems(QDialog):
    """viewing royalty and invoice items"""

    def __init__(self):
        super().__init__()

    def BookInvoiceItems(self):
        self.setWindowTitle("View Book Invoice Items")
        self.setModal(True)
        self.setFixedSize(640, 220)
        self.vertical = QVBoxLayout(self)
        self.vertical.addWidget(self.table)
        self.btnCalculate.setFixedSize(100, 40)
        self.btnUpdateBookInvoiceItems.setFixedSize(100, 40)
        self.btnDeleteEntry.setFixedSize(100, 40)
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.btnCalculate)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnUpdateBookInvoiceItems)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnDeleteEntry)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        
        self.exec_()
        
    def BookInvoiceItemsButtons(self):
        self.btnCalculate = QPushButton("Calculate", self)
        self.btnUpdateBookInvoiceItems = QPushButton("Update Book \n Invoice Items", self)
        self.btnDeleteEntry = QPushButton("Delete \n Entry", self)  

    def RoyaltiesItems(self):
        self.setWindowTitle("View Royalty Items")
        self.setModal(True)
        self.setFixedSize(640, 220)
        self.vertical = QVBoxLayout(self)
        self.vertical.addWidget(self.table)
        self.btnCalculate.setFixedSize(100, 40)
        self.btnUpdateRoyaltyItems.setFixedSize(100, 40)
        self.btnDeleteEntry.setFixedSize(100, 40)
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.btnCalculate)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnUpdateRoyaltyItems)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnDeleteEntry)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        
        self.exec_()
        
    def RoyaltyItemsButtons(self):
        self.btnCalculate = QPushButton("Calculate", self)
        self.btnUpdateRoyaltyItems = QPushButton("Update \n Royalty Items", self)
        self.btnDeleteEntry = QPushButton("Delete \n Entry", self)        











    def CalculateBookInvoiceItems(self):
        
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")

            i = 1
            while i != 0:

                try:
                    self.selection = "BookInvoiceQuantity, BookInvoiceDiscount, ShippingPrice, ISBN, Price"
                    self.tables = "BookInvoiceItems, Book"
                    sql = "select {}, from {} where BookInvoiceID = {}, BookInvoiceItemsID = {}, ISBN = {}".format(self.selection, self.tables, self.selectedID, i, self.selectedISBN)
                    cursor.execute(sql)
                    self.SelectionList = list(cursor.fetchall())
                    i += 1
                    print(self.SelectionList) 
                except:
                    #sql = "update BookInvoice set BookInvoicePayment = {} where BookInvoiceID = {}".format(BookInvoicePayment, BookInvoiceID)
                    #cursor.execute(sql)
                    #db.commit()
                    i = 0
