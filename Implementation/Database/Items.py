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
            self.BookInvoicePayment = 0
            i = 1
            while i != 0:
                try:
                    Selection = "BookInvoiceItems.BookInvoiceQuantity, BookInvoiceItems.BookInvoiceDiscount, BookInvoiceItems.ShippingPrice, Book.Price"
                    Tables = "BookInvoiceItems, Book"
                    sql = "select {} from {} where BookInvoiceItems.BookInvoiceID = {} and BookInvoiceItems.BookInvoiceItemsID = {} and Book.ISBN = {}".format(Selection, Tables, self.selectedID, i, self.selectedISBN)
                    cursor.execute(sql)
                    self.SelectionList = list(cursor.fetchone())
                    i += 1
                    
                    self.Quantity = self.SelectionList[0]
                    self.Discount = self.SelectionList[1] / 100
                    self.ShippingPrice = self.SelectionList[2]
                    self.Price = self.SelectionList[3]
                    
                    self.TempPayment = (self.Quantity * self.Price)
                    self.Discount = self.TempPayment * self.Discount
                    self.TempPayment -= self.Discount
                    self.TempPayment += self.ShippingPrice

                    self.BookInvoicePayment += self.TempPayment
                except:
                    sql = "update BookInvoice set BookInvoicePayment = '{}' where BookInvoiceID = {}".format(self.BookInvoicePayment, self.selectedID)
                    cursor.execute(sql)
                    db.commit()
                    i = 0

    def CalculateRoyaltyItems(self):
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            self.RoyaltyPayment = 0
            i = 1
            
        while i != 0:
            
            try:
                Select1 = "RoyaltyItems.Currency, RoyaltyItems.NetSales, RoyaltyItems.ExcRateFromGBP, RoyaltyItems.RoyaltyQuantity, "
                Select2 = "Book.NoOfPages, Book.Size, Book.Cover, Book.Back"
                Tables = "RoyaltyItems, Book"
                sql = "select {}{} from {} where RoyaltiesID = {} and RoyaltyItemsID = {} and ISBN = {}".format(Select1, Select2, Tables, self.selectedID, i, self.SelectedISBN)
                cursor.execute(sql)
                self.SelectionList = list(cursor.fetchone())
                self.Currency = self.SelectionList[0]                
                self.NetSales = float(self.SelectionList[1])
                self.Quantity = self.SelectionList[3]
                self.NoOfPages = int(self.SelectionList[4])
                self.Size = self.SelectionList[5]
                self.Cover = self.SelectionList[6]
                self.Back = self.Selection[7]


                if self.Size == "Large":
                    self.PagePrice = 0.015 * self.NoOfPages
                    if self.Back == "Hard":
                        self.CoverPrice = 5
                    elif self.Back == "Soft":
                        self.CoverPrice = 1
                elif self.Size == "Small":
                    self.PagePrice = 0.01 * self.NoOfPages
                    if self.Back == "Hard":
                        self.CoverPrice = 4
                    elif self.Back == "Soft":
                        self.CoverPrice = 0.7
                        
                self.PrintCost = (self.PagePrice + self.CoverPrice) * self.Quantity
                
                self.TempPayment= self.NetSales - self.PrintCost
                i += 1
                self.RoyaltyPayment += self.TempPayment
            except:
                self.RoyaltyPayment = self.TempPayment
                if self.Currency != "£":
                    self.ExcRateFromGBP = float(self.SelectionList[2])
                    self.RoyaltyPayment /= self.ExcRateFromGBP
                sql = "update Royalties set RoyaltyPayment = {} where RoyaltiesID = {}".format(self.RoyaltyPayment, self.selectedID)
                cursor.execute(sql)
                db.commit()
                i = 0
