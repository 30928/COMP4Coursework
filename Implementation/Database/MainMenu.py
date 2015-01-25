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
from CalendarWidget import *

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
        self.CurrentTable = "Customer"            
        self.MainMenuButtons.setLayout(self.MainMenuButtons.vertical)

        self.StackedLayout = QStackedLayout()     
        
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.StackedLayout)
        self.setCentralWidget(self.centralWidget)

        self.StackedLayout.addWidget(self.MainMenuButtons)   
    
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
        self.MainMenuButtons.btnUpdateEntry.clicked.connect(self.UpdateCustomerEntry)
        self.MenuBar.add_entry.triggered.connect(self.AddEntry)
        self.MenuBar.remove_entry.triggered.connect(self.RemoveEntry)
        self.MenuBar.update_entry.triggered.connect(self.UpdateCustomerEntry)
        self.ViewWindow.btnBack.clicked.connect(self.Back)
        self.ViewWindow.btnAddBook.clicked.connect(self.AddItem)
        self.ViewWindow.btnUpdateBook.clicked.connect(self.UpdateEntry)
        self.ViewWindow.btnDeleteBook.clicked.connect(self.RemoveFromDB)
        self.ViewWindow.btnViewPubInvoice.clicked.connect(self.ViewPubInvoice)
        self.ViewWindow.btnViewBookInvoices.clicked.connect(self.ViewBookInvoice)
        

        
    def AddToDB(self):
        self.input_data = [] #input data list
        if self.CurrentTable == "Book":
            self.TableValues = "Book (ISBN, AuthorID, BookTitle, NoOfPages, Size, Back, Cover, Paper, Font, FontSize, DatePublished, Price)"
            self.Placeholders = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.NoOfEntries = 12

        elif self.CurrentTable == "PubInvoice":
            self.TableValues = "PubInvoice (ISBN, AuthorID, PubInvoiceDate, PubInvoiceService, PubInvoicePayment)"
            self.Placeholders = "(?, ?, ?, ?, ?)"
            self.NoOfEntries = 5

        elif self.CurrentTable == "BookInvoice":
            self.TableValues = "BookInvoice (AuthorID, BookInvoiceDate, BookInvoicePayment)"
            self.Placeholders = "(?, ?, ?)"
            self.NoOfEntries = 3
            
        for count in range(0, self.NoOfEntries):
            try:
                self.input_data.append(str(self.AddWindow.inputList[count].currentText()))
            except:
                self.input_data.append(self.AddWindow.inputList[count].text())
                        

        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            self.sql = "insert into {} values {}".format(self.TableValues, self.Placeholders)
            cursor.execute(self.sql, self.input_data)
            db.commit()


    def RemoveFromDB(self):
        #getting primary key of the row
        self.ConfirmDialog = dbConfirmationDialog()
        self.ConfirmDialog.DeleteMsg = self.CurrentTable
        self.SelectedAuthorID = self.SelectedID
        
        if self.CurrentTable == "Book":
            self.SelectedRow = self.ViewWindow.table.currentRow()
            self.SelectedID = QTableWidgetItem(self.ViewWindow.table.item(self.SelectedRow, 0)).text()
            self.SelectedIDName = "ISBN"
            self.ConfirmDialog.Msg = "Are you sure you want to delete this book?"
            self.ConfirmDialog.ConfirmedMsg = "Book was successfully deleted"
            
        elif self.CurrentTable == "PubInvoice":
            self.SelectedRow = self.PubInvoiceWindow.table.currentRow()
            self.SelectedID = QTableWidgetItem(self.PubInvoiceWindow.table.item(self.SelectedRow, 0)).text()
            self.SelectedIDName = "PubInvoiceID"
            self.ConfirmDialog.Msg = "Are you sure you want to delete this Invoice?"
            self.ConfirmDialog.ConfirmedMsg = "Invoice was successfully deleted"

        elif self.CurrentTable == "BookInvoice":
            self.SeletedRow = self.BookInvoiceWindow.table.currentRow()
            self.selectedID = QTableWidgetItem(self.BookInvoiceWindow.table.item(self.SelectedRow, 0)).text()
            self.SelectedIDName = "BookInvoiceID"
            self.ConfirmDialog.Msg = "Are uou sure you want to delete this Invoice?"
            self.ConfirmDialog.ConfirmedMsg = "Invoice was successfully deleted"

        self.ConfirmDialog.VerifyDlg()
            
        if self.ConfirmDialog.ConfirmedDialog.Accepted == True:
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                #cursor.execute("PRAGMA foreign_keys = ON")
                sql = "delete from {} where {} = '{}'".format(self.CurrentTable, self.SelectedIDName, self.SelectedID)
                cursor.execute(sql)
                db.commit()

        self.SelectedID = self.SelectedAuthorID
            
        if self.CurrentTable == "Book":
            self.ViewWindow.table.sql = "select * from Book where AuthorID = {}".format(self.SelectedAuthorID)
            self.ViewWindow.table.initTable()

        elif self.CurrentTable == "PubInvoice":
            self.PubInvoiceWindow.table.sql = "select * from PubInvoice where ISBN = {}".format(self.SelectedISBN)
            self.PubInvoiceWindow.table.initTable()

        elif self.CurrentTable == "BookInvoice":
            self.BookInvoiceWindow.table.sql = "select * from BookInvoice where AuthorID = {}".format(self.SelectedAuthorID)
            self.BookInvoiceWindow.table.initTable()

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


    def AddItem(self):
        self.AddWindow = dbAddItemWindow()
        self.AddWindow.setFixedSize(360,200)
        self.AddWindow.AnswerButtons()
        self.AddWindow.btnConfirm.clicked.connect(self.AddToDB)
        self.AddWindow.Editing = False

        if self.CurrentTable == "Book":
            self.AddWindow.sql = "select * from Book"
            
        elif self.CurrentTable == "PubInvoice":
            self.AddWindow.setFixedSize(400,150)
            self.AddWindow.sql = "select ISBN, AuthorID, PubInvoiceDate, PubInvoiceService, PubInvoicePayment from PubInvoice"
            self.AddWindow.selectedISBN = self.SelectedISBN

        elif self.CurrentTable == "BookInvoice":
            self.AddWindow.sql = "select AuthorID, BookinvoiceDate, BookInvoicePayment from BookInvoice"
            self.AddWindow.setFixedSize(350,100)
            
        self.AddWindow.AddType = self.CurrentTable
        self.AddWindow.selectedID = self.SelectedID
        self.AddWindow.CalendarWidget = dbCalendarWidget()
        self.AddWindow.CalendarWidget.Calendar()
        self.AddWindow.initAddItemWindow()
        if self.CurrentTable == "Book":
            self.ViewWindow.table.initTable()
        elif self.CurrentTable == "PubInvoice":
            self.PubInvoiceWindow.table.initTable()
            self.PubInvoiceWindow.table.setFixedSize(620, 150)
        elif self.CurrentTable == "BookInvoice":
            self.BookInvoiceWindow.table.initTable()


            
    def ViewPubInvoice(self):
        self.CurrentTable = "PubInvoice"
        self.ViewWindow.SelectedRow = self.ViewWindow.table.currentRow()
        self.SelectedISBN = QTableWidgetItem(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, 0)).text()
        if self.SelectedISBN != "":
            self.PubInvoiceWindow = dbRoyaltiesAndInvoices()
            self.PubInvoiceWindow.PubInvoiceButtons()
            self.PubInvoiceWindow.btnAddPubInvoice.clicked.connect(self.AddItem)
            self.PubInvoiceWindow.btnUpdatePubInvoice.clicked.connect(self.UpdateEntry)
            self.PubInvoiceWindow.btnDeleteEntry.clicked.connect(self.RemoveFromDB)
            self.PubInvoiceWindow.table = dbTableWidget()
            self.PubInvoiceWindow.table.sql = "select * from PubInvoice where ISBN = {}".format(self.SelectedISBN)
            self.PubInvoiceWindow.table.initTable()
            self.PubInvoiceWindow.table.setFixedSize(620, 150)
            self.PubInvoiceWindow.PubInvoice()
            self.CurrentTable = "Book"

    def ViewBookInvoice(self):
        self.CurrentTable = "BookInvoice"
        self.ViewWindow.SelectedRow = self.ViewWindow.table.currentRow()
        self.SelectedISBN = QTableWidgetItem(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, 0)).text()
        self.SelectedID = QTableWidgetItem(self.TableWidget.item(self.TableWidget.currentRow(), 0)).text()
        if self.SelectedISBN != "":
            self.BookInvoiceWindow = dbRoyaltiesAndInvoices()
            self.BookInvoiceWindow.BookInvoiceButtons()
            self.BookInvoiceWindow.btnAddBookInvoice.clicked.connect(self.AddItem)
            self.BookInvoiceWindow.btnUpdateBookInvoice.clicked.connect(self.UpdateEntry)
            self.BookInvoiceWindow.btnDeleteEntry.clicked.connect(self.RemoveFromDB)
            self.BookInvoiceWindow.table = dbTableWidget()
            self.BookInvoiceWindow.table.sql = "select * from BookInvoice where AuthorID = {}".format(self.SelectedID)
            self.BookInvoiceWindow.table.initTable()
            self.BookInvoiceWindow.table.setFixedSize(620, 150)
            self.BookInvoiceWindow.BookInvoice()
            self.CurrentTable = "Book"

    def Back(self):
        self.ViewWindow.table.selectedID = None
        self.CurrentTable = "Customer"
        self.StackedLayout.setCurrentIndex(0)
        self.MenuBar.setVisible(True)

    
    def RefreshTable(self): #refreshes customer table
        self.TableWidget.initTable()


    def AddEntry(self): #customer entry
        self.AddEntryWindow = dbAddEntryWindow()
        self.AddEntryWindow.initAddEntryWindow()
        self.RefreshTable()


    def UpdateCustomerEntry(self): #for customer entries only
        self.SelectedRow = self.TableWidget.currentRow()
        self.SelectedAuthorID = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 0)).text()
  
        if self.SelectedAuthorID != "":
            self.UpdateEntryWindow = dbUpdateEntryWindow()
            self.UpdateEntryWindow.setFixedSize(640, 115)
            self.UpdateEntryWindow.selectedID = self.SelectedAuthorID
            self.UpdateEntryWindow.table = dbTableWidget()
            self.selectText = "Firstname, Lastname, Email, Phonenumber, Address, Postcode"
            self.UpdateEntryWindow.table.sql = "select {} from Customer where AuthorID = {}".format(self.selectText, self.SelectedAuthorID)
            self.SelectedID = self.SelectedAuthorID 
            self.UpdateEntryWindow.table.initTable()
            self.UpdateEntryWindow.table.setFixedSize(617, 55)
            self.UpdateEntryWindow.Verify = dbConfirmationDialog()
            self.UpdateEntryWindow.initConfirmBtn()
            self.UpdateEntryWindow.btnConfirm.clicked.connect(self.VerifyCustomerUpdate)
            self.UpdateEntryWindow.initUpdateEntryWindowDlg()
        self.RefreshTable()

    def UpdateEntry(self): #for all entries
        self.Selection = False
        self.EditWindow = dbAddItemWindow() #uses the add window to init same interface but fill boxes with data
        self.EditWindow.setFixedSize(360, 200)
        self.EditWindow.AnswerButtons()

        self.EditWindow.btnConfirm.clicked.connect(self.VerifyUpdate)
        self.EditWindow.originalItemList = []
        
        if self.CurrentTable == "Book":
            self.EditWindow.sql = "select * from Book"
            for count in range(0, 12): #fetching existing data from table
                self.ViewWindow.SelectedRow = self.ViewWindow.table.currentRow()
                self.EditWindow.originalItemList.append(QTableWidgetItem(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, count)).text())
                if self.ViewWindow.SelectedRow != -1:
                    self.Selection = True
        elif self.CurrentTable == "PubInvoice":
            self.EditWindow.setFixedSize(400,150)
            self.EditWindow.selectedISBN = self.SelectedISBN
            self.EditWindow.sql = "select ISBN, AuthorID, PubInvoiceDate, PubInvoiceService, PubInvoicePayment from PubInvoice"
            for count in range(1, 6): #fetching existing data from table
                self.PubInvoiceWindow.SelectedRow = self.PubInvoiceWindow.table.currentRow()
                self.EditWindow.originalItemList.append(QTableWidgetItem(self.PubInvoiceWindow.table.item(self.PubInvoiceWindow.SelectedRow, count)).text())
                if self.PubInvoiceWindow.SelectedRow != -1:
                    self.Selection = True
        elif self.CurrentTable == "BookInvoice":
            self.EditWindow.setFixedSize(350, 100)
            self.EditWindow.selectedID = self.SelectedID
            self.EditWindow.sql = "select AuthorID, BookInvoiceDate, BookInvoicePayment from BookInvoice".format(self.SelectedID)
            for count in range(1, 4): #fetching existing data from table
                self.BookInvoiceWindow.SelectedRow = self.BookInvoiceWindow.table.currentRow()
                self.EditWindow.originalItemList.append(QTableWidgetItem(self.BookInvoiceWindow.table.item(self.BookInvoiceWindow.SelectedRow, count)).text())
                if self.BookInvoiceWindow.SelectedRow != -1:
                    self.Selection = True
        self.EditWindow.Editing = True

        if self.Selection == True:
                
            self.EditWindow.AddType = self.CurrentTable
            self.EditWindow.selectedID = self.SelectedID
            self.EditWindow.CalendarWidget = dbCalendarWidget()
            self.EditWindow.CalendarWidget.Calendar()
            self.EditWindow.initAddItemWindow()

        
    def VerifyCustomerUpdate(self):
        self.UpdateEntryWindow.Verify = dbConfirmationDialog()
        #new instance for customer verification

    def VerifyUpdate(self):
        self.EditWindow.Verify = dbConfirmationDialog()
        self.EditWindow.Verify.Msg = "Insert Password to confirm all changes"
        self.EditWindow.Verify.ConfirmedMsg = "Update successful"
        self.EditWindow.Verify.VerifyDlg()
        if self.EditWindow.Verify.ConfirmedDialog.Accepted == True:
            self.UpdateChanges()
            self.EditWindow.accept()
            
        
    def UpdateChanges(self):
        UL = [] #UL = Update List
        self.SelectedAuthorID = self.SelectedID
        if self.CurrentTable == "Book":
            self.NoOfEntries = 12
            self.ID = "ISBN"
            self.SelectedISBN = QTableWidgetItem(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, 0)).text()
            self.SelectedID = self.SelectedISBN

        elif self.CurrentTable == "PubInvoice":
            self.NoOfEntries = 5
            self.ID = "PubInvoiceID"
            self.SelectedID = QTableWidgetItem(self.PubInvoiceWindow.table.item(self.PubInvoiceWindow.SelectedRow, 0)).text()

        elif self.CurrentTable == "BookInvoice":
            self.NoOfEntries = 3
            self.ID = "BookInvoiceID"
            self.SelectedID = QTableWidgetItem(self.BookInvoiceWindow.table.item(self.BookInvoiceWindow.SelectedRow, 0)).text()
        
        for count in range(0, self.NoOfEntries):
            try:
                UL.append(str(self.EditWindow.inputList[count].currentText()))
            except:
                UL.append(self.EditWindow.inputList[count].text())
                
        if self.CurrentTable == "Book":       
            self.Update1 = "ISBN = '{}', AuthorID = '{}', BookTitle = '{}', NoOfPages = '{}', Size = '{}', Back = '{}',".format(UL[0], UL[1], UL[2], UL[3], UL[4], UL[5])
            self.Update2 = " Cover = '{}', Paper = '{}', Font = '{}', FontSize = '{}', DatePublished = '{}', Price = '{}'".format(UL[6], UL[7], UL[8], UL[9], UL[10], UL[11])
            self.Update = self.Update1 + self.Update2
            
        elif self.CurrentTable == "PubInvoice":
            self.Update = "ISBN = '{}', AuthorID = '{}', PubInvoiceDate = '{}', PubInvoiceService = '{}', PubInvoicePayment = '{}'".format(UL[0], UL[1], UL[2], UL[3], UL[4])

        elif self.CurrentTable == "BookInvoice":
            self.Update = "AuthorID = '{}', BookInvoiceDate = '{}', BookInvoicePayment = '{}'".format(UL[0], UL[1], UL[2])
        
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "update {} set {} where {} = {}".format(self.CurrentTable, self.Update, self.ID, self.SelectedID)
            cursor.execute(sql)
            db.commit()
            
        self.SelectedID = self.SelectedAuthorID
        
        if self.CurrentTable == "Book":
            self.ViewWindow.table.initTable()
        elif self.CurrentTable == "PubInvoice":
            self.PubInvoiceWindow.table.initTable()
        elif self.CurrentTable == "BookInvoice":
            self.BookInvoiceWindow.table.initTable()

        
    def RemoveEntry(self):
        self.SelectedRow = self.TableWidget.currentRow()
        self.ConfirmDialog = dbConfirmationDialog()
        self.ConfirmDialog.SelectedAuthorID = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 0)).text() #getting AuthorID of a row
        if self.ConfirmDialog.SelectedAuthorID != "":
            self.Firstname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 1)).text()
            self.Lastname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 2)).text()
            self.ConfirmDialog.Name = "{} {}".format(self.Firstname, self.Lastname)
            self.ConfirmDialog.Msg = "Are you sure you want to delete {} and all records about them?".format(self.ConfirmDialog.Name)
            self.ConfirmDialog.ConfirmedMsg = "{}'s records have been successfully erased.".format(self.ConfirmDialog.Name)
            self.ConfirmDialog.VerifyDlg()
        
            if self.ConfirmDialog.ConfirmedDialog.Accepted == True:
                with sqlite3.connect("PP.db") as db:
                    cursor = db.cursor()
                    cursor.execute("PRAGMA foreign_keys = ON")
                    sql = "delete from Customer where AuthorID = {}".format(self.ConfirmDialog.SelectedAuthorID)
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
