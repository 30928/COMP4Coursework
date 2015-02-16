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
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setHorizontalSpacing(10)
        self.setFixedSize(400, 200)
        self.leFirstname = QLineEdit(self)
        self.leLastname = QLineEdit(self)
        self.cbTable = QComboBox(self)
        self.cbCategory = QComboBox(self)
        self.btnDate = QPushButton("Add Date", self)
        self.leSearch = QLineEdit(self)
        self.btnCancel = QPushButton("Cancel", self)
        self.btnSearch = QPushButton("Search", self)
        self.btnDate.setFixedSize(75, 20)
        self.lblFirstname = QLabel("Author Firstname:")
        self.lblLastname = QLabel("Author Lastname:")
        self.gridLayout.addWidget(self.leFirstname, 0, 3)
        self.gridLayout.addWidget(self.leLastname, 1, 3)
        self.gridLayout.addWidget(self.lblFirstname, 0, 2, Qt.AlignRight)
        self.gridLayout.addWidget(self.lblLastname, 1, 2, Qt.AlignRight)
        self.gridLayout.addWidget(self.cbTable, 0, 0)
        self.gridLayout.addWidget(self.cbCategory, 2, 0)
        self.gridLayout.addWidget(self.btnDate, 2, 2, Qt.AlignHCenter)
        self.gridLayout.addWidget(self.leSearch, 2, 3)
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
        self.cbCategory.activated[str].connect(self.DateButton)
        self.btnDate.hide()
        self.leSearch.hide()
        self.CalendarWidget.btnSelect.clicked.connect(self.getDate)
        self.btnDate.clicked.connect(self.CalendarWidget.DisplayCalendar)
        self.leSearch.setFixedSize(self.leSearch.sizeHint())
        self.leFirstname.setFixedSize(self.leFirstname.sizeHint())
        self.leLastname.setFixedSize(self.leLastname.sizeHint())
        self.btnSearch.clicked.connect(self.getSearchData)
        self.btnCancel.clicked.connect(self.reject)
        self.exec_()
        
    def ChangeCategories(self):
        self.btnDate.hide()
        self.leSearch.show()
        self.cbCategory.clear()
        if self.cbTable.currentText() == "Author":
            self.leSearch.hide()
        elif self.cbTable.currentText() == "Book":
            self.cbCategory.addItem("Book Title")
            self.cbCategory.addItem("Price")
            self.cbCategory.addItem("Date Published")
            
        elif self.cbTable.currentText() == "Publishing Invoice":
            self.cbCategory.addItem("Service")
            self.cbCategory.addItem("Date")
            
        elif self.cbTable.currentText() == "Book Invoice":
            self.cbCategory.addItem("Date")
            self.btnDate.show()
            
        elif self.cbTable.currentText() == "Book Invoice Items":
            self.cbCategory.addItem("Quantity")
            self.cbCategory.addItem("Discount")
            self.cbCategory.addItem("Shipping Type")
            
        elif self.cbTable.currentText() == "Royalties":
            self.cbCategory.addItem("Date")
            self.btnDate.show()
            
        elif self.cbTable.currentText() == "Royalty Items":
            self.cbCategory.addItem("Quantity")
            self.cbCategory.addItem("Discount")
            self.cbCategory.addItem("Currency")

    def DateButton(self):
        if self.cbCategory.currentText()[:4] == "Date":
            self.btnDate.show()
            self.leSearch.setReadOnly(True)
        else:
            self.btnDate.hide()
            self.leSearch.setReadOnly(False)
            
    def getDate(self):
        self.CalendarWidget.date = self.CalendarWidget.qle.text()
        self.leSearch.setText(self.CalendarWidget.date)

    def getSearchData(self):
        self.Valid = True
        self.Firstname = self.leFirstname.text()
        self.Lastname = self.leLastname.text()
        self.Table = self.cbTable.currentText().replace(" ", "")
        if self.Table == "PublishingInvoice":
            self.Table = "PubInvoice"
            
        if self.Table != "Author":
            self.Category = self.cbCategory.currentText().replace(" ", "")
            self.Search = self.leSearch.text()
            
            if self.Firstname.replace(" ", "") == "" or self.Lastname.replace(" ", "") == "" or self.Category == "" or self.Search.replace(" ", "") == "":
                self.Msg = QMessageBox()
                self.Msg.setWindowTitle("Invalid Entry")
                self.Msg.setText("You must fill in all fields.")
                self.Msg.exec_()
                self.Valid = False


            if self.Category in ["Discount", "Quantity"]:

                if self.Table == "RoyaltyItems":
                    self.Category = "Royalty{}".format(self.Category)
                    
                elif self.Table == "BookInvoiceItems":
                    self.Category = "BookInvoice{}".format(self.Category)
                    
            elif self.Category == "Date":
                self.Category = "{}Date".format(self.Table)
                
            elif self.Category == "Service":
                self.Category = "PubInvoiceService"
                

            
            if self.Table not in ["BookInvoiceItems", "RoyaltyItems"]:
                if self.Table in ["PubInvoice", "Royalties", "BookInvoice"]:
                    self.sql = "select Customer.AuthorID, {0}ID from Customer, {0} where (Customer.Firstname like '{1}%' or Customer.Lastname like '{2}%') and {0}.{3} like '{4}%' and Customer.AuthorID = {0}.AuthorID".format(self.Table, self.Firstname, self.Lastname, self.Category, self.Search)
                elif self.Table == "Book":
                    self.sql = "select Customer.AuthorID, Book.AuthorID, Book.ISBN from Customer, {0} where (Customer.Firstname like '{1}%' or Customer.Lastname like '{2}%') and {0}.{3} like '{4}%' and Customer.AuthorID = {0}.AuthorID".format(self.Table, self.Firstname, self.Lastname, self.Category, self.Search)

            else:
                self.sql = "select Customer.AuthorID, Book.AuthorID, Book.ISBN, {0}.ISBN, {0}ID from Customer, Book, {0} where (Customer.Firstname like '{1}%' or Customer.Lastname like '{2}%') and {0}.{3} like '{4}%' and Customer.AuthorID = Book.AuthorID and Book.ISBN = {0}.ISBN".format(self.Table, self.Firstname, self.Lastname, self.Category, self.Search)

        else:
            
            if self.Firstname.replace(" ", "") == "" or self.Lastname.replace(" ", "") == "":
                self.Msg = QMessageBox()
                self.Msg.setWindowTitle("Invalid Entry")
                self.Msg.setText("You must fill enter the Firstname and Lastname")
                self.Msg.exec_()
                self.Valid = False
                
            self.Table = "Customer" #Author table is referred to as 'Customer'
            self.sql = "select AuthorID from Customer where Firstname like '{0}%' or Lastname like '{1}%'".format(self.Firstname, self.Lastname)

        if self.Valid == True:
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                cursor.execute(self.sql)
                self.Results = list(cursor.fetchall())
            self.accept()
