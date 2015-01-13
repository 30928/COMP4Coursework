from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class dbTableWidget(QTableWidget):
    """main table widget"""

    def __init__(self):
        super().__init__()
        
    def initTable(self):
        #adding table widget
        self.setFixedSize(716,275)
        
    def CustomerTable(self):
        
        self.clear()
        self.setColumnCount(7)
        self.setRowCount(1)
        
        CustomerHeaders = ["AuthorID", "Forename", "Surname", "Email", "Phonenumber", "Address", "Postcode"]
        self.setHorizontalHeaderLabels(CustomerHeaders)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        with sqlite3.connect("PP.db") as db: #fetching all customer data from db
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")
            
            sql = "select all AuthorID from Customer" 
            cursor.execute(sql)
            self.AuthorIDList = list(cursor.fetchall())

            sql = "select all Firstname from Customer" 
            cursor.execute(sql)
            self.FirstnameList = list(cursor.fetchall())

            sql = "select all Lastname from Customer" 
            cursor.execute(sql)
            self.LastnameList = list(cursor.fetchall())

            sql = "select all Email from Customer" 
            cursor.execute(sql)
            self.EmailList = list(cursor.fetchall())
            
            sql = "select all Phonenumber from Customer" 
            cursor.execute(sql)
            self.PhonenumberList = list(cursor.fetchall())

            sql = "select all Address from Customer" 
            cursor.execute(sql)
            self.AddressList = list(cursor.fetchall())

            sql = "select all Postcode from Customer" 
            cursor.execute(sql)
            self.PostcodeList = list(cursor.fetchall())
            
        self.setRowCount(len(self.AuthorIDList))

        for count in range(0, int(len(self.AuthorIDList))): #adding to the main table
            self.AuthorID = self.AuthorIDList[count]
            self.AuthorID = list(self.AuthorID)[0]
            self.setItem(count, 0, QTableWidgetItem(str(self.AuthorID)))

            self.Firstname = self.FirstnameList[count]
            self.Firstname = list(self.Firstname)[0]
            self.setItem(count, 1, QTableWidgetItem(str(self.Firstname)))
            
            self.Lastname = self.LastnameList[count]
            self.Lastname = list(self.Lastname)[0]
            self.setItem(count, 2, QTableWidgetItem(str(self.Lastname)))

            self.Email = self.EmailList[count]
            self.Email = list(self.Email)[0]
            self.setItem(count, 3, QTableWidgetItem(str(self.Email)))

            self.Phonenumber = self.PhonenumberList[count]
            self.Phonenumber = list(self.Phonenumber)[0]
            self.setItem(count, 4, QTableWidgetItem(str(self.Phonenumber)))

            self.Address = self.AddressList[count]
            self.Address = list(self.Address)[0]
            self.setItem(count, 5, QTableWidgetItem(str(self.Address)))

            self.Postcode = self.PostcodeList[count]
            self.Postcode = list(self.Postcode)[0]
            self.setItem(count, 6, QTableWidgetItem(str(self.Postcode)))

    def BookTable(self):
        self.clear()
        self.setColumnCount(12)
        self.setRowCount(1)
        
        BookHeaders = ["AuthorID", "ISBN", "Book Title", "No Of Pages", "Size", "Back", "Cover", "Paper", "Font", "Font size", "Date Pulished", "Price"]
        self.setHorizontalHeaderLabels(BookHeaders)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        with sqlite3.connect("PP.db") as db: #fetching all book data from db
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")
            
            sql = "select all AuthorID from Book" 
            cursor.execute(sql)
            self.AuthorIDList = list(cursor.fetchall())

            sql = "select all ISBN from Book" 
            cursor.execute(sql)
            self.ISBNList = list(cursor.fetchall())

            sql = "select all BookTitle from Book" 
            cursor.execute(sql)
            self.BookTitleList = list(cursor.fetchall())

            sql = "select all NoOfPages from Book" 
            cursor.execute(sql)
            self.NoOfPagesList = list(cursor.fetchall())
            
            sql = "select all Size from Book" 
            cursor.execute(sql)
            self.SizeList = list(cursor.fetchall())

            sql = "select all Back from Book" 
            cursor.execute(sql)
            self.BackList = list(cursor.fetchall())

            sql = "select all Cover from Book" 
            cursor.execute(sql)
            self.CoverList = list(cursor.fetchall())

            sql = "select all Paper from Book" 
            cursor.execute(sql)
            self.PaperList = list(cursor.fetchall())

            sql = "select all Font from Book" 
            cursor.execute(sql)
            self.FontList = list(cursor.fetchall())

            sql = "select all FontSize from Book" 
            cursor.execute(sql)
            self.FontSizeList = list(cursor.fetchall())

            sql = "select all DatePublished from Book" 
            cursor.execute(sql)
            self.DatePubList = list(cursor.fetchall())

            sql = "select all Price from Book" 
            cursor.execute(sql)
            self.PriceList = list(cursor.fetchall())
            
        self.setRowCount(len(self.AuthorIDList))

        for count in range(0, int(len(self.AuthorIDList))): #adding to the table
            self.AuthorID = self.AuthorIDList[count]
            self.AuthorID = list(self.AuthorID)[0]
            self.setItem(count, 0, QTableWidgetItem(str(self.AuthorID)))

            self.ISBN = self.ISBNList[count]
            self.ISBN = list(self.ISBN)[0]
            self.setItem(count, 1, QTableWidgetItem(str(self.ISBN)))
            
            self.BookTitle = self.BookTitleList[count]
            self.BookTitle = list(self.BookTitle)[0]
            self.setItem(count, 2, QTableWidgetItem(str(self.BookTitle)))

            self.NoOfPages = self.NoOfPagesList[count]
            self.NoOfPages = list(self.NoOfPages)[0]
            self.setItem(count, 3, QTableWidgetItem(str(self.NoOfPages)))

            self.Size = self.SizeList[count]
            self.Size = list(self.Size)[0]
            self.setItem(count, 4, QTableWidgetItem(str(self.Size)))

            self.Size = self.SizeList[count]
            self.Size = list(self.Size)[0]
            self.setItem(count, 5, QTableWidgetItem(str(self.Size)))

            self.Back = self.BackList[count]
            self.Back = list(self.Back)[0]
            self.setItem(count, 6, QTableWidgetItem(str(self.Back)))

            self.Cover = self.CoverList[count]
            self.Cover = list(self.Cover)[0]
            self.setItem(count, 6, QTableWidgetItem(str(self.Cover)))

            self.Paper = self.PaperList[count]
            self.Paper = list(self.Paper)[0]
            self.setItem(count, 6, QTableWidgetItem(str(self.Paper)))

            self.Font = self.FontList[count]
            self.Font = list(self.Font)[0]
            self.setItem(count, 6, QTableWidgetItem(str(self.Font)))

            self.FontSize = self.FontSizeList[count]
            self.FontSize = list(self.FontSize)[0]
            self.setItem(count, 6, QTableWidgetItem(str(self.FontSize)))

            self.DatePub = self.DatePubList[count]
            self.DatePub = list(self.DatePub)[0]
            self.setItem(count, 6, QTableWidgetItem(str(self.DatePub)))

            self.Price = self.PriceList[count]
            self.Price = list(self.Price)[0]
            self.setItem(count, 6, QTableWidgetItem(str(self.Price)))
        


        
