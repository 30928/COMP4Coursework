from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
from MenuBar import *
from initMainMenuButtons import *
from AddEntryWindow import *
from TableWidget import *
from ConfirmationDialog import *
from ViewWindow import *
from AddItemWindow import *
from ViewRoyaltiesAndInvoices import *
from UpdateEntryWindow import *

class MainWindow(QMainWindow):
    """main window"""

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Main Menu")
        self.setFixedSize(735,400)
        self.MenuBar = dbMenuBar()
        self.setMenuBar(self.MenuBar)
        
        self.TableWidget = dbTableWidget()
        self.TableWidget.sql = "select * from Customer"
        self.TableWidget.initTable()
        
        self.MainMenuButtons = initMainMenuButtons()
        self.MainMenuButtons.vertical.addLayout(self.MainMenuButtons.horizontalTop)
        self.MainMenuButtons.vertical.addWidget(self.TableWidget)
        self.MainMenuButtons.vertical.addLayout(self.MainMenuButtons.horizontalBottom)
            
        self.MainMenuButtons.setLayout(self.MainMenuButtons.vertical)

        self.StackedLayout = QStackedLayout()     
        
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.StackedLayout)
        self.setCentralWidget(self.centralWidget)

        self.StackedLayout.addWidget(self.MainMenuButtons)
        self.StackedLayout.setCurrentIndex(1)
        

        
        self.ViewWindow = dbViewWindow()
        self.ViewWindow.View()
        self.ViewWindow.vertical.addLayout(self.ViewWindow.horizontalTop)
        self.ViewWindow.table = dbTableWidget()
        self.ViewWindow.vertical.addWidget(self.ViewWindow.table)
        self.ViewWindow.vertical.addLayout(self.ViewWindow.horizontalBottom)
        self.ViewWindow.setLayout(self.ViewWindow.vertical)
        
        self.StackedLayout.addWidget(self.ViewWindow)
        
        #connections
        self.MainMenuButtons.btnAddEntry.clicked.connect(self.AddEntry) 
        self.MainMenuButtons.btnRemoveEntry.clicked.connect(self.RemoveEntry)
        self.MainMenuButtons.btnView.clicked.connect(self.ViewCustomer)
        self.MainMenuButtons.btnUpdateEntry.clicked.connect(self.UpdateCustomer)
        self.ViewWindow.btnBack.clicked.connect(self.Back)
        self.ViewWindow.btnAddBook.clicked.connect(self.AddBookWindow)
        self.ViewWindow.btnDeleteBook.clicked.connect(self.RemoveFromDB)
        self.ViewWindow.btnViewPubInvoice.clicked.connect(self.ViewPubInvoice)
        
    def AddToDB(self):
        idl = [] #input data list
        self.input_data = ""
        if self.AddBookWindow.AddType == "Book":
            self.TableValues = "Book (ISBN, AuthorID, BookTitle, NoOfPages, Size, Back, Cover, Paper, Font, FontSize, DatePublished, Price)"
            self.Placeholders = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            for count in range(0, 12):
                try:
                    idl.append(str(self.AddBookWindow.inputList[count].currentText()))
                except:
                    idl.append(self.AddBookWindow.inputList[count].text())
            self.input_data = (idl[0], idl[1], idl[2], idl[3], idl[4], idl[5], idl[6], idl[7], idl[8], idl[9], idl[10], idl[11])
        
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            self.sql = "insert into {} values {}".format(self.TableValues, self.Placeholders)
            cursor.execute(self.sql, self.input_data)
            db.commit()

    def RemoveFromDB(self):
        #getting primary key of the row
        if self.CurrentTable == "Book":
            self.SelectedRow = self.ViewWindow.table.currentRow()
            self.SelectedAuthorID = self.SelectedID
            self.SelectedID = QTableWidgetItem(self.ViewWindow.table.item(self.SelectedRow, 0)).text()
            self.SelectedIDName = "ISBN"

        self.ConfirmDialog = ConfirmationDialog()
        self.ConfirmDialog.DeleteMsg = self.CurrentTable
        self.ConfirmDialog.Name = "{} {}".format(self.Firstname, self.Lastname)
        self.ConfirmDialog.RemoveDlg()
        if self.ConfirmDialog.ConfirmedDialog.Accepted == True:
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                sql = "delete from {} where {} = '{}'".format(self.CurrentTable, self.SelectedIDName, self.SelectedID)
                cursor.execute(sql)
                db.commit()

        self.ViewWindow.table.sql = "select * from Book where AuthorID = {}".format(self.SelectedAuthorID)
        self.ViewWindow.table.initTable()

    def AddBookWindow(self):
        self.AddBookWindow = dbAddItemWindow()
        self.AddBookWindow.AnswerButtons()
        self.AddBookWindow.btnConfirm.clicked.connect(self.AddToDB)
        self.AddBookWindow.sql = "select * from Book"
        self.AddBookWindow.AddType = "Book"
        self.AddBookWindow.selectedID = self.SelectedID
        self.AddBookWindow.initAddItemWindow()
        self.ViewWindow.table.initTable()
        
    def ViewCustomer(self):
        self.SelectedRow = self.TableWidget.currentRow()
        self.SelectedID = QTableWidgetItem(self.TableWidget.item(self.TableWidget.currentRow(), 0)).text()
        self.Firstname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 1)).text()
        self.Lastname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 2)).text()
  
        if self.SelectedID != "":   
            self.ViewWindow.table.sql = "select * from Book where AuthorID = {}".format(self.SelectedID)
            self.ViewWindow.table.initTable()
            self.CurrentTable = "Book"
            self.StackedLayout.setCurrentIndex(1)
            self.MenuBar.setVisible(False)

    def ViewPubInvoice(self):
        self.ViewWindow.SelectedRow = self.ViewWindow.table.currentRow()
        self.SelectedISBN = QTableWidgetItem(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, 0)).text()
        if self.SelectedISBN != "":
            self.PubInvoiceWindow = dbRoyaltiesAndInvoices()
            self.PubInvoiceWindow.table = dbTableWidget()
            self.PubInvoiceWindow.table.sql = "select * from PubInvoice where ISBN = {}".format(self.SelectedISBN)
            self.PubInvoiceWindow.table.initTable()
            self.PubInvoiceWindow.table.setFixedSize(620, 150)
            self.PubInvoiceWindow.PubInvoice()      
            
    def Back(self):
        self.ViewWindow.table.selectedID = None
        self.CurrentTable = "Customer"
        self.StackedLayout.setCurrentIndex(0)
        self.MenuBar.setVisible(True)
    
    def RefreshTable(self): #refreshing table to show changes made
        self.TableWidget.initTable()

    def AddEntry(self):
        self.AddEntryWindow = dbAddEntryWindow()
        self.AddEntryWindow.initAddEntryWindow()
        self.RefreshTable()

    def UpdateCustomer(self):
        self.SelectedRow = self.TableWidget.currentRow()
        self.SelectedAuthorID = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 0)).text()
        if self.SelectedAuthorID != "":
            self.UpdateEntryWindow = dbUpdateEntryWindow()

            self.UpdateEntryWindow.table = dbTableWidget()
            self.UpdateEntryWindow.table.sql = "select Firstname, Lastname, Email, Phonenumber, Address, Postcode from Customer where AuthorID = {}".format(self.SelectedAuthorID)
            self.UpdateEntryWindow.table.initTable()
            self.UpdateEntryWindow.table.setFixedSize(630, 55)
            self.UpdateEntryWindow.initUpdateEntryWindowDlg()
            
            
    def RemoveEntry(self):
        self.SelectedRow = self.TableWidget.currentRow()
        self.SelectedAuthorID = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 0)).text() #getting AuthorID of a row
        
        self.ConfirmDialog = ConfirmationDialog()
        self.ConfirmDialog.DeleteMsg = "customer and all records about them?"
        self.Firstname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 1)).text()
        self.Lastname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 2)).text()
        self.ConfirmDialog.Name = "{} {}".format(self.Firstname, self.Lastname)
        self.ConfirmDialog.RemoveDlg()
        
        if self.ConfirmDialog.ConfirmedDialog.Accepted == True:
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                sql = "delete from Customer where AuthorID = {}".format(self.SelectedAuthorID)
                cursor.execute(sql)
                db.commit()
        self.RefreshTable()
        
def main():
    app = QApplication(sys.argv)
    launcher = MainWindow()
    launcher.raise_()
    launcher.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
