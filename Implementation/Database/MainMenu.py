from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
from MenuBar import *
from initMainMenuButtons import *
from AddEntryWindow import *
class MainWindow(QMainWindow):
    """main window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setFixedSize(735,400)
        self.initMenuBar() #initialising the menu bar
        self.initButtons() #initialising main menu buttons
    
    def initButtons(self):
        initMainMenuButtons.Buttons(self)

    def initMenuBar(self):
        MenuBar.MenuBar(self)

    def initTable(self):
                                    
        self.table = QTableWidget() #creating main menu table
        self.table.setFixedSize(716,275)
        self.table.clear()
        self.table.setColumnCount(7)
        CustomerHeaders = ["AuthorID", "Firstname", "Lastname", "Email", "Phonenumber", "Address", "Postcode"]
        self.table.setHorizontalHeaderLabels(CustomerHeaders)
        self.vertical.addWidget(self.table)
        self.initCustomers()
        
    def initCustomers(self):
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
            
        self.table.setRowCount(len(self.AuthorIDList))

        for count in range(0, int(len(self.AuthorIDList))): #adding to the main table
            self.AuthorID = self.AuthorIDList[count]
            self.AuthorID = list(self.AuthorID)[0]
            self.table.setItem(count, 0, QTableWidgetItem(str(self.AuthorID)))

            self.Firstname = self.FirstnameList[count]
            self.Firstname = list(self.Firstname)[0]
            self.table.setItem(count, 1, QTableWidgetItem(str(self.Firstname)))
            
            self.Lastname = self.LastnameList[count]
            self.Lastname = list(self.Lastname)[0]
            self.table.setItem(count, 2, QTableWidgetItem(str(self.Lastname)))

            self.Email = self.EmailList[count]
            self.Email = list(self.Email)[0]
            self.table.setItem(count, 3, QTableWidgetItem(str(self.Email)))

            self.Phonenumber = self.PhonenumberList[count]
            self.Phonenumber = list(self.Phonenumber)[0]
            self.table.setItem(count, 4, QTableWidgetItem(str(self.Phonenumber)))

            self.Address = self.AddressList[count]
            self.Address = list(self.Address)[0]
            self.table.setItem(count, 5, QTableWidgetItem(str(self.Address)))

            self.Postcode = self.PostcodeList[count]
            self.Postcode = list(self.Postcode)[0]
            self.table.setItem(count, 6, QTableWidgetItem(str(self.Postcode)))

    def RefreshTable(self): #refreshing table to show changes made
        self.initCustomers()
        
def main():
    app = QApplication(sys.argv)
    launcher = MainWindow()
    launcher.raise_()
    launcher.show()
    app.exec_()
    
if __name__ == "__main__":
    main()