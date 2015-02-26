from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
import subprocess

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
from Items import *
from SearchDatabase import *
from LoginDB import *
from ChangePassword import *
from UsernameOrPassword import *
from ChangeUsername import *
from SearchResults import *

class MainWindow(QMainWindow):
    """main window"""

    def __init__(self, Username):
        super().__init__()
        self.Username = Username
        self.setWindowTitle("Main Menu")
        self.setWindowIcon(QIcon("PPIcon.png"))
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
    
        self.ViewWindow = dbViewWindow() #instantiating view window
        self.ViewWindow.View()
        self.ViewWindow.vertical.addLayout(self.ViewWindow.horizontalTop)
        self.ViewWindow.table = dbTableWidget()
        self.ViewWindow.vertical.addWidget(self.ViewWindow.table)
        self.ViewWindow.vertical.addLayout(self.ViewWindow.horizontalBottom)
        self.ViewWindow.setLayout(self.ViewWindow.vertical)
        
        self.StackedLayout.addWidget(self.ViewWindow)
        
        self.SearchResults = initSearchResultsMenu()
        self.StackedLayout.addWidget(self.SearchResults)
        self.SearchTable = dbTableWidget()
        self.SearchResults.vertical.addWidget(self.SearchTable)

        #connections
        self.MainMenuButtons.btnAddEntry.clicked.connect(self.AddEntry) 
        self.MainMenuButtons.btnRemoveEntry.clicked.connect(self.RemoveEntry)
        self.MainMenuButtons.btnView.clicked.connect(self.ViewCustomer)
        self.MainMenuButtons.btnUpdateEntry.clicked.connect(self.UpdateCustomerEntry)
        self.MainMenuButtons.btnQuickSearch.clicked.connect(self.QuickSearch)
        self.MainMenuButtons.btnSearchdb.clicked.connect(self.Search)
        self.MainMenuButtons.btnLogOut.clicked.connect(self.LogOut)
        self.MainMenuButtons.btnChangePassword.clicked.connect(self.ChangeUsernameOrPassword)
        self.MenuBar.search_database.triggered.connect(self.Search)
        self.MenuBar.add_entry.triggered.connect(self.AddEntry)
        self.MenuBar.remove_entry.triggered.connect(self.RemoveEntry)
        self.MenuBar.update_entry.triggered.connect(self.UpdateCustomerEntry)
        self.MenuBar.log_out.triggered.connect(self.LogOut)
        self.MenuBar.change_password.triggered.connect(self.ChangeUsernameOrPassword)
        self.ViewWindow.btnBack.clicked.connect(self.Back)
        self.ViewWindow.btnAddBook.clicked.connect(self.AddItem)
        self.ViewWindow.btnUpdateBook.clicked.connect(self.UpdateEntry)
        self.ViewWindow.btnDeleteBook.clicked.connect(self.RemoveFromDB)
        self.ViewWindow.btnViewPubInvoice.clicked.connect(self.ViewPubInvoice)
        self.ViewWindow.btnViewBookInvoices.clicked.connect(self.ViewBookInvoice)
        self.ViewWindow.btnViewRoyalties.clicked.connect(self.ViewRoyalties)
        self.SearchResults.btnBack.clicked.connect(self.Back)


    def AddEntry(self): #adding customer entry 
        self.AddEntryWindow = dbAddEntryWindow()
        self.AddEntryWindow.Added = False
        self.AddEntryWindow.initAddEntryWindow()
        self.RefreshTables()



    def AddItem(self): #initialising an add window for getting inputs for other entries
        self.AddWindow = dbAddItemWindow()
        self.AddWindow.setFixedSize(360,200)
        self.AddWindow.AddType = self.CurrentTable
        self.AddWindow.AnswerButtons()
        self.AddWindow.Editing = False

        if self.CurrentTable == "Book":
            self.AddWindow.sql = "select * from Book"
            
        elif self.CurrentTable == "PubInvoice":
            self.AddWindow.setFixedSize(400,150)
            self.AddWindow.sql = "select ISBN, AuthorID, PubInvoiceDate, PubInvoiceService, PubInvoicePayment from PubInvoice"
            self.AddWindow.selectedISBN = self.SelectedISBN

        elif self.CurrentTable == "BookInvoice":
            self.AddWindow.sql = "select AuthorID, BookinvoiceDate from BookInvoice"
            self.AddWindow.setFixedSize(350,100)

        elif self.CurrentTable == "Royalties":
            self.AddWindow.sql = "select AuthorID, RoyaltiesDate from Royalties"
            self.AddWindow.setFixedSize(350,100)
            
        elif self.CurrentTable == "BookInvoiceItems":
            self.AddWindow.sql = "select BookInvoiceID, ISBN, BookInvoiceQuantity, BookInvoiceDiscount, ShippingType, ShippingPrice from BookInvoiceItems"
            self.AddWindow.setFixedSize(450, 150)
            self.AddWindow.selectedISBN = self.SelectedISBN
            self.Editing = False
            self.AddWindow.btnCalculate.clicked.connect(self.BookInvoiceItemCalculation)
            
        elif self.CurrentTable == "RoyaltyItems":
            self.AddWindow.sql = "select RoyaltiesID, ISBN, Currency, RoyaltyDiscount, WholesalePrice, RoyaltyQuantity, PrintCost, ExcRateFromGBP from RoyaltyItems"
            self.AddWindow.setFixedSize(450, 250)
            self.AddWindow.selectedISBN = self.SelectedISBN
            self.Editing = False
            self.AddWindow.btnCalculate.clicked.connect(self.RoyaltyItemCalculation)
            
        self.AddWindow.selectedID = self.SelectedID
        self.AddWindow.CalendarWidget = dbCalendarWidget()
        self.AddWindow.CalendarWidget.Calendar()
        
        self.AddWindow.initAddItemWindow()
        try:
            if self.AddWindow.Valid == True: #inputs must pass validation before being added
                self.AddToDB()
        except AttributeError:
            pass #exception of window being closed
        self.RefreshTables()

    def RecalculateItems(self): #recalculates after changes
        if self.CurrentTable == "BookInvoiceItems": 
            self.BookInvoiceItemsWindow.CalculateBookInvoiceItems()
            self.CurrentTable = "BookInvoice"
            self.RefreshTables()
            self.CurrentTable = "BookInvoiceItems"
                
        elif self.CurrentTable == "RoyaltyItems" or self.BookEdited == True:
            self.RoyaltyItemsWindow.CalculateRoyaltyItems()
            self.CurrentTable = "Royalties"
            self.RefreshTables()
            self.CurrentTable = "RoyaltyItems"


        
    def AddToDB(self): #Adding Entries to database
        self.input_data = []
        if self.CurrentTable == "Book":
            self.TableValues = "Book (ISBN, AuthorID, BookTitle, NoOfPages, Size, Back, Cover, Paper, Font, FontSize, DatePublished, Price)"
            self.Placeholders = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.NoOfEntries = 12

        elif self.CurrentTable == "PubInvoice":
            self.TableValues = "PubInvoice (ISBN, AuthorID, PubInvoiceDate, PubInvoiceService, PubInvoicePayment)"
            self.Placeholders = "(?, ?, ?, ?, ?)"
            self.NoOfEntries = 5

        elif self.CurrentTable == "BookInvoice":
            self.TableValues = "BookInvoice (AuthorID, BookInvoiceDate)"
            self.Placeholders = "(?, ?)"
            self.NoOfEntries = 2

        elif self.CurrentTable == "Royalties":
            self.TableValues = "Royalties (AuthorID, RoyaltiesDate)"
            self.Placeholders = "(?, ?)"
            self.NoOfEntries = 2
            
        elif self.CurrentTable == "BookInvoiceItems":
            self.TableValues = "BookInvoiceItems (BookInvoiceID, ISBN, BookInvoiceQuantity, BookInvoiceDiscount, ShippingType, ShippingPrice)"
            self.Placeholders = "(?, ?, ?, ?, ?, ?)"
            self.NoOfEntries = 6

        elif self.CurrentTable == "RoyaltyItems":
            self.TableValues = "RoyaltyItems (RoyaltiesID, ISBN, Currency, RoyaltyDiscount, WholesalePrice, RoyaltyQuantity, PrintCost, ExcRateFromGBP, NetSales)"
            self.Placeholders = "(?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.NoOfEntries = 9
            
        for count in range(0, self.NoOfEntries):
            try: #putting the input data in a list
                self.input_data.append(str(self.AddWindow.inputList[count].currentText()))
            except:
                if count == 8 and self.CurrentTable == "RoyaltyItems":
                    self.input_data.append(self.NetSales) #Net sales are calculated, as opposed to being entered
                else:
                    self.input_data.append(self.AddWindow.inputList[count].text())

        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            self.sql = "insert into {} values {}".format(self.TableValues, self.Placeholders)
            cursor.execute(self.sql, self.input_data)
            db.commit()
            
        self.RefreshTables()
            
        try:
            self.RecalculateItems()
        except:
            pass
        
    def RemoveEntry(self): #removing a customer
        self.SelectedRow = self.TableWidget.currentRow()
        self.ConfirmDialog = dbConfirmationDialog()
        self.ConfirmDialog.Username = self.Username
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
                    sql = "select ISBN from Book where AuthorID = {}".format(self.ConfirmDialog.SelectedAuthorID)
                    cursor.execute(sql)
                    self.ISBNDeletion = list(cursor.fetchall())
                    for count in range(0, len(self.ISBNDeletion)): #removes all customer details, starting with foreign keys for referential integrity
                        sql = "delete from BookInvoiceItems where ISBN = {}".format(list(list(self.ISBNDeletion)[count])[0])
                        cursor.execute(sql)
                        sql = "delete from RoyaltyItems where ISBN = {}".format(list(list(self.ISBNDeletion)[count])[0])
                        cursor.execute(sql)
                    sql = "delete from PubInvoice where AuthorID = {}".format(self.ConfirmDialog.SelectedAuthorID)
                    cursor.execute(sql)
                    sql = "delete from BookInvoice where AuthorID = {}".format(self.ConfirmDialog.SelectedAuthorID)
                    cursor.execute(sql)
                    sql = "delete from Royalties where AuthorID = {}".format(self.ConfirmDialog.SelectedAuthorID)
                    cursor.execute(sql)
                    sql = "delete from Book where AuthorID = {}".format(self.ConfirmDialog.SelectedAuthorID)
                    cursor.execute(sql)
                    sql = "delete from Customer where AuthorID = {}".format(self.ConfirmDialog.SelectedAuthorID)
                    cursor.execute(sql)
                    db.commit()
                    self.RefreshTables()



    def RemoveFromDB(self): #removing other entries
        #getting primary key of the row
        self.ConfirmDialog = dbConfirmationDialog()
        self.ConfirmDialog.Username = self.Username
        self.ConfirmDialog.DeleteMsg = self.CurrentTable
        self.SelectedAuthorID = self.SelectedID
        
        if self.CurrentTable == "Book":
            self.ForeignKeyMsg = "Royalties and Invoices"
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
            self.ForeignKeyMsg = "Book Invoice Items"
            self.SelectedRow = self.BookInvoiceWindow.table.currentRow()
            self.SelectedID = QTableWidgetItem(self.BookInvoiceWindow.table.item(self.SelectedRow, 0)).text()
            self.SelectedIDName = "BookInvoiceID"
            self.ConfirmDialog.Msg = "Are you sure you want to delete this Invoice?"
            self.ConfirmDialog.ConfirmedMsg = "Invoice was successfully deleted"

        elif self.CurrentTable == "Royalties":
            self.ForeignKeyMsg = "Royalty Items"
            self.SelectedRow = self.RoyaltiesWindow.table.currentRow()
            self.SelectedID = QTableWidgetItem(self.RoyaltiesWindow.table.item(self.SelectedRow, 0)).text()
            self.SelectedIDName = "RoyaltiesID"
            self.ConfirmDialog.Msg = "Are you sure you want to delete this Entry?"
            self.ConfirmDialog.ConfirmedMsg = "Entry was successfully deleted"

        elif self.CurrentTable == "BookInvoiceItems":
            self.SelectedRow = self.BookInvoiceItemsWindow.table.currentRow()
            self.SelectedID = QTableWidgetItem(self.BookInvoiceItemsWindow.table.item(self.SelectedRow, 0)).text()
            self.SelectedIDName = "BookInvoiceItemsID"
            self.ConfirmDialog.Msg = "Are you sure you want to delete this Item?"
            self.ConfirmDialog.ConfirmedMsg = "Item was successfully deleted"

        elif self.CurrentTable == "RoyaltyItems":
            self.SelectedRow = self.RoyaltyItemsWindow.table.currentRow()
            self.SelectedID = QTableWidgetItem(self.RoyaltyItemsWindow.table.item(self.SelectedRow, 0)).text()
            self.SelectedIDName = "RoyaltyItemsID"
            self.ConfirmDialog.Msg = "Are you sure you want to delete this Item?"
            self.ConfirmDialog.ConfirmedMsg = "Item was successfully deleted"
        self.ConfirmDialog.Prevention = True #deletion may be prevented if integrity error occurs
        if self.SelectedRow != -1:
            self.ConfirmDialog.VerifyDlg() #verification
            try:
                if self.ConfirmDialog.ConfirmedDialog.Accepted == True:
                    with sqlite3.connect("PP.db") as db:
                        cursor = db.cursor()
                        cursor.execute("PRAGMA foreign_keys = ON")
                        sql = "delete from {} where {} = '{}'".format(self.CurrentTable, self.SelectedIDName, self.SelectedID)
                        cursor.execute(sql)
                        db.commit()
                        self.ConfirmDialog.ConfirmedDialog.Confirmed()
            except sqlite3.IntegrityError:
                self.Msg = QMessageBox()
                self.Msg.setWindowTitle("Error")
                self.Msg.setText("You must delete all the {} first.".format(self.ForeignKeyMsg))
                self.Msg.exec_() #informs user that selected entry cannot be deleted and what must be done for it to be deleted
            self.SelectedID = self.SelectedAuthorID
            self.RefreshTables()

            try:
                self.RecalculateItems()
            except:
                pass


        
    def ViewCustomer(self): #displaying customer data
        self.SelectedRow = self.TableWidget.currentRow()
        self.SelectedID = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 0)).text()
        self.Firstname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 1)).text()
        self.Lastname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 2)).text()
  
        if self.SelectedID != "":
            self.SelectedAuthorID = self.SelectedID
            self.CurrentTable = "Book"
            self.RefreshTables()
            self.StackedLayout.setCurrentIndex(1)
            self.MenuBar.setVisible(False)


        
    def ViewPubInvoice(self): #initialising the view publishing invoice window
        self.CurrentTable = "PubInvoice"
        self.ViewWindow.SelectedRow = self.ViewWindow.table.currentRow()
        self.SelectedISBN = QTableWidgetItem(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, 0)).text()
        self.SelectedID = QTableWidgetItem(self.TableWidget.item(self.TableWidget.currentRow(), 0)).text()
        self.SelectedAuthorID = self.SelectedID
        if self.SelectedISBN != "":
            self.PubInvoiceWindow = dbRoyaltiesAndInvoices()
            self.PubInvoiceWindow.PubInvoiceButtons()
            self.PubInvoiceWindow.btnAddPubInvoice.clicked.connect(self.AddItem)
            self.PubInvoiceWindow.btnUpdatePubInvoice.clicked.connect(self.UpdateEntry)
            self.PubInvoiceWindow.btnDeleteEntry.clicked.connect(self.RemoveFromDB)
            self.PubInvoiceWindow.table = dbTableWidget()
            self.RefreshTables()
            self.PubInvoiceWindow.table.setFixedSize(620, 150)
            self.PubInvoiceWindow.PubInvoice()
        self.CurrentTable = "Book"



    def ViewBookInvoice(self): #initialising the view book invoice window
        self.CurrentTable = "BookInvoice"
        self.ViewWindow.SelectedRow = self.ViewWindow.table.currentRow()
        self.SelectedISBN = QTableWidgetItem(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, 0)).text()
        self.SelectedAuthorID = QTableWidgetItem(self.TableWidget.item(self.TableWidget.currentRow(), 0)).text()

        if self.SelectedISBN != "":
            self.BookInvoiceWindow = dbRoyaltiesAndInvoices()
            self.BookInvoiceWindow.BookInvoiceButtons()
            self.BookInvoiceWindow.btnViewBookInvoiceItems.clicked.connect(self.ViewBookInvoiceItems)
            self.BookInvoiceWindow.btnAddBookInvoice.clicked.connect(self.AddItem)
            self.BookInvoiceWindow.btnUpdateBookInvoice.clicked.connect(self.UpdateEntry)
            self.BookInvoiceWindow.btnDeleteEntry.clicked.connect(self.RemoveFromDB)
            self.BookInvoiceWindow.table = dbTableWidget()
            self.RefreshTables()
            self.BookInvoiceWindow.table.setFixedSize(620, 150)
            self.BookInvoiceWindow.BookInvoice()
        self.CurrentTable = "Book"



    def ViewBookInvoiceItems(self): #initialising the view book invoice items window
        self.CurrentTable = "BookInvoiceItems"
        self.BookInvoiceWindow.SelectedRow = self.BookInvoiceWindow.table.currentRow()
        self.holder = self.SelectedAuthorID
        self.SelectedAuthorID = self.SelectedID
        self.BookInvoiceWindow.selectedISBN = self.SelectedISBN
        self.SelectedID = QTableWidgetItem(self.BookInvoiceWindow.table.item(self.BookInvoiceWindow.SelectedRow, 0)).text()

        if self.SelectedID != "":
            self.BookInvoiceItemsWindow = dbItems()
            self.BookInvoiceItemsWindow.selectedID = self.SelectedID
            self.BookInvoiceItemsWindow.selectedISBN = self.SelectedISBN
            self.BookInvoiceItemsWindow.BookInvoiceItemsButtons()
            self.BookInvoiceItemsWindow.btnCalculate.clicked.connect(self.AddItem)
            self.BookInvoiceItemsWindow.btnUpdateBookInvoiceItems.clicked.connect(self.UpdateEntry)
            self.BookInvoiceItemsWindow.btnDeleteEntry.clicked.connect(self.RemoveFromDB)
            self.BookInvoiceItemsWindow.table = dbTableWidget()
            self.RefreshTables()
            self.BookInvoiceItemsWindow.table.setFixedSize(620, 150)
            self.BookInvoiceItemsWindow.BookInvoiceItems()
        self.SelectedID = self.SelectedAuthorID
        self.SelectedAuthorID = self.holder
        self.CurrentTable = "BookInvoice"
        self.RefreshTables()



    def ViewRoyalties(self): #initialising the view royalties window
        self.CurrentTable = "Royalties"
        self.ViewWindow.SelectedRow = self.ViewWindow.table.currentRow()
        self.SelectedISBN = QTableWidgetItem(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, 0)).text()
        self.SelectedAuthorID = QTableWidgetItem(self.TableWidget.item(self.TableWidget.currentRow(), 0)).text()
        if self.SelectedISBN != "":
            self.RoyaltiesWindow = dbRoyaltiesAndInvoices()
            self.RoyaltiesWindow.RoyaltiesButtons()
            self.RoyaltiesWindow.btnViewRoyaltyItems.clicked.connect(self.ViewRoyaltyItems)
            self.RoyaltiesWindow.btnAddRoyalties.clicked.connect(self.AddItem)
            self.RoyaltiesWindow.btnUpdateRoyalties.clicked.connect(self.UpdateEntry)
            self.RoyaltiesWindow.btnDeleteEntry.clicked.connect(self.RemoveFromDB)
            self.RoyaltiesWindow.table = dbTableWidget()
            self.RefreshTables()
            self.RoyaltiesWindow.table.setFixedSize(620, 150)
            self.RoyaltiesWindow.Royalties()
        self.CurrentTable = "Book"
        
    def ViewRoyaltyItems(self): #initialising the view royalty items window
        self.CurrentTable = "RoyaltyItems"
        self.RoyaltiesWindow.SelectedRow = self.RoyaltiesWindow.table.currentRow()
        self.holder = self.SelectedAuthorID
        self.SelectedAuthorID = self.SelectedID
        self.RoyaltiesWindow.selectedISBN = self.SelectedISBN
        self.SelectedID = QTableWidgetItem(self.RoyaltiesWindow.table.item(self.RoyaltiesWindow.SelectedRow, 0)).text()

        if self.SelectedID != "":
            self.RoyaltyItemsWindow = dbItems()
            self.RoyaltyItemsWindow.selectedID = self.SelectedID
            self.RoyaltyItemsWindow.selectedISBN = self.SelectedISBN
            self.RoyaltyItemsWindow.RoyaltyItemsButtons()
            self.RoyaltyItemsWindow.btnCalculate.clicked.connect(self.AddItem)
            self.RoyaltyItemsWindow.btnUpdateRoyaltyItems.clicked.connect(self.UpdateEntry)
            self.RoyaltyItemsWindow.btnDeleteEntry.clicked.connect(self.RemoveFromDB)
            self.RoyaltyItemsWindow.table = dbTableWidget()
            self.RefreshTables()
            self.RoyaltyItemsWindow.table.setFixedSize(620, 150)
            self.RoyaltyItemsWindow.RoyaltiesItems()
        self.SelectedID = self.SelectedAuthorID
        self.SelectedAuthorID = self.holder
        self.CurrentTable = "Royalties"
        self.RefreshTables()


        
    def BookInvoiceItemCalculation(self): #calculating the bookinvoicepayment
        try:
            if self.Editing == False:
                self.Quantity = int(self.AddWindow.inputList[2].text())
                self.Discount = float(self.AddWindow.inputList[3].text()) / 100
                self.ShippingPrice = float(self.AddWindow.inputList[5].text())
                self.ISBN = self.AddWindow.inputList[1].text()
            elif self.Editing == True:
                self.Quantity = int(self.EditWindow.inputList[2].text())
                self.Discount = float(self.EditWindow.inputList[3].text()) / 100
                self.ShippingPrice = float(self.EditWindow.inputList[5].text())
                self.ISBN = self.EditWindow.inputList[1].text()

            with sqlite3.connect("PP.db") as db: #fetching data from db
                cursor = db.cursor()
                cursor.execute("select Price from Book where ISBN = {}".format(self.ISBN))
                self.Price = list(cursor.fetchone())[0]
                db.commit()

            self.BookInvoiceItemPayment = (self.Quantity * self.Price)
            self.Discount = self.BookInvoiceItemPayment * self.Discount
            self.BookInvoiceItemPayment -= self.Discount
            self.BookInvoiceItemPayment += self.ShippingPrice
            self.BookInvoiceItemPayment = "£{0:.2f}".format(self.BookInvoiceItemPayment)
            if self.Editing == False:
                self.AddWindow.btnConfirm.clicked.connect(self.AddWindow.accept)
                self.AddWindow.qleCalculation.setText(self.BookInvoiceItemPayment)
            elif self.Editing == True:
                if self.EditWindow.Calculated == False:
                    self.EditWindow.Calculated = True #prevents duplicate connections
                    self.EditWindow.btnConfirm.clicked.connect(self.VerifyUpdate)
                self.EditWindow.qleCalculation.setText(self.BookInvoiceItemPayment)
        except:
            self.Msg = QMessageBox()
            self.Msg.setWindowTitle("Error")
            self.Msg.setText("You must fill all fields before clicking 'Calculate'.")
            self.Msg.exec_()

    def RoyaltyItemCalculation(self): #calculating the royalty payment
        try:
            if self.Editing == False:
                self.Currency = self.AddWindow.inputList[2].text()
                self.WholesalePrice = float(self.AddWindow.inputList[4].text())
                self.Quantity = int(self.AddWindow.inputList[5].text())
                self.PrintCost = float(self.AddWindow.inputList[6].text())
            elif self.Editing == True:
                self.Currency = self.EditWindow.inputList[2].text()
                self.WholesalePrice = float(self.EditWindow.inputList[4].text())
                self.Quantity = int(self.EditWindow.inputList[5].text())
                self.PrintCost = float(self.EditWindow.inputList[6].text())

            self.NetSales = self.WholesalePrice * self.Quantity
            self.RoyaltyItemPayment = self.NetSales - self.PrintCost
            self.RoyaltyItemPayment = "{0:.2f}".format(self.RoyaltyItemPayment)
            if self.Editing == False:
                self.AddWindow.btnConfirm.clicked.connect(self.AddWindow.accept)
                self.AddWindow.qleCalculation.setText("{}{}".format(self.Currency, self.RoyaltyItemPayment))
                self.AddWindow.NetSales = self.NetSales
            elif self.Editing == True:
                if self.EditWindow.Calculated == False:
                    self.EditWindow.Calculated = True #prevents duplicate connections
                    self.EditWindow.btnConfirm.clicked.connect(self.VerifyUpdate)
                self.EditWindow.qleCalculation.setText("{}{}".format(self.Currency, self.RoyaltyItemPayment))
                self.EditWindow.NetSales = self.NetSales
        except:
            self.Msg = QMessageBox()
            self.Msg.setWindowTitle("Error")
            self.Msg.setText("You must fill all fields before clicking 'Calculate'.")
            self.Msg.exec_()

            
    def UpdateCustomerEntry(self): #updating customer entries only
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
            self.UpdateEntryWindow.Verify.Username = self.Username
            self.UpdateEntryWindow.initConfirmBtn()
            self.UpdateEntryWindow.btnConfirm.clicked.connect(self.VerifyCustomerUpdate)
            self.UpdateEntryWindow.initUpdateEntryWindowDlg()
            self.TableWidget.sql = "select * from Customer"
            self.RefreshTables()



    def UpdateEntry(self): #getting the update input
        self.Selection = False
        self.EditWindow = dbAddItemWindow() #uses the add window to init same interface but fill boxes with data
        self.EditWindow.setFixedSize(360, 200)
        self.EditWindow.AddType = self.CurrentTable
        self.EditWindow.AnswerButtons()
        self.EditWindow.ReadyToVerify = False
        self.EditWindow.originalItemList = []
        
        if self.CurrentTable == "Book":
            self.EditWindow.sql = "select * from Book"
            self.ViewWindow.SelectedRow = self.ViewWindow.table.currentRow()
            if self.ViewWindow.SelectedRow != -1:
                self.Selection = True
                with sqlite3.connect("PP.db") as db:
                    cursor = db.cursor() #fetching data from database for the edit window
                    sql = "select * from Book where ISBN = {}".format(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, 0).text())
                    cursor.execute(sql)
                    self.EditWindow.originalItemList = list(cursor.fetchone())
                    
        elif self.CurrentTable == "PubInvoice":
            self.EditWindow.setFixedSize(400,150)
            self.EditWindow.selectedISBN = self.SelectedISBN
            self.EditWindow.sql = "select ISBN, AuthorID, PubInvoiceDate, PubInvoiceService, PubInvoicePayment from PubInvoice"
            self.PubInvoiceWindow.SelectedRow = self.PubInvoiceWindow.table.currentRow()
            if self.PubInvoiceWindow.SelectedRow != -1:
                self.Selection = True
                with sqlite3.connect("PP.db") as db:
                    cursor = db.cursor() #fetching data from database for the edit window
                    sql = "select ISBN, AuthorID, PubInvoiceDate, PubInvoiceService, PubInvoicePayment from PubInvoice where PubInvoiceID = {}".format(self.PubInvoiceWindow.table.item(self.PubInvoiceWindow.SelectedRow, 0).text())
                    cursor.execute(sql)
                    self.EditWindow.originalItemList = list(cursor.fetchone())
                
        elif self.CurrentTable == "BookInvoice":
            self.EditWindow.setFixedSize(350, 100)
            self.EditWindow.selectedID = self.SelectedID
            self.EditWindow.sql = "select AuthorID, BookInvoiceDate from BookInvoice"
            self.BookInvoiceWindow.SelectedRow = self.BookInvoiceWindow.table.currentRow()
            if self.BookInvoiceWindow.SelectedRow != -1:
                self.Selection = True
                with sqlite3.connect("PP.db") as db:
                    cursor = db.cursor() #fetching data from database for the edit window
                    sql = "select AuthorID, BookInvoiceDate from BookInvoice where BookInvoiceID = {}".format(self.BookInvoiceWindow.table.item(self.BookInvoiceWindow.SelectedRow, 0).text())
                    cursor.execute(sql)
                    self.EditWindow.originalItemList = list(cursor.fetchone())
                
        elif self.CurrentTable == "Royalties":
            self.EditWindow.setFixedSize(350, 100)
            self.EditWindow.selectedID = self.SelectedID
            self.EditWindow.sql = "select AuthorID, RoyaltiesDate from Royalties"
            self.RoyaltiesWindow.SelectedRow = self.RoyaltiesWindow.table.currentRow()
            if self.RoyaltiesWindow.SelectedRow != -1:
                self.Selection = True
                with sqlite3.connect("PP.db") as db:
                    cursor = db.cursor() #fetching data from database for the edit window
                    sql = "select AuthorID, RoyaltiesDate from Royalties where RoyaltiesID = {}".format(self.RoyaltiesWindow.table.item(self.RoyaltiesWindow.SelectedRow, 0).text())
                    cursor.execute(sql)
                    self.EditWindow.originalItemList = list(cursor.fetchone())
                
        elif self.CurrentTable == "BookInvoiceItems":
            self.EditWindow.setFixedSize(450, 150)
            self.EditWindow.selectedID = self.SelectedID
            self.Editing = True
            self.EditWindow.btnCalculate.clicked.connect(self.BookInvoiceItemCalculation)
            self.EditWindow.selectedISBN = self.SelectedISBN
            self.EditWindow.sql = "select BookInvoiceID, ISBN, BookInvoiceQuantity, BookInvoiceDiscount, ShippingType, ShippingPrice from BookInvoiceItems"
            self.BookInvoiceItemsWindow.SelectedRow = self.BookInvoiceItemsWindow.table.currentRow()
            if self.BookInvoiceItemsWindow.SelectedRow != -1:
                self.Selection = True
                with sqlite3.connect("PP.db") as db:
                    cursor = db.cursor() #fetching data from database for the edit window
                    sql = "select BookInvoiceID, ISBN, BookInvoiceQuantity, BookInvoiceDiscount, ShippingType, ShippingPrice from BookInvoiceItems where BookInvoiceItemsID = {}".format(self.BookInvoiceItemsWindow.table.item(self.BookInvoiceItemsWindow.SelectedRow, 0).text())
                    cursor.execute(sql)
                    self.EditWindow.originalItemList = list(cursor.fetchone())

        elif self.CurrentTable == "RoyaltyItems":
            self.EditWindow.setFixedSize(450, 250)
            self.EditWindow.selectedID = self.SelectedID
            self.Editing = True
            self.EditWindow.btnCalculate.clicked.connect(self.RoyaltyItemCalculation)
            self.EditWindow.selectedISBN = self.SelectedISBN
            self.EditWindow.sql = "select RoyaltiesID, ISBN, Currency, RoyaltyDiscount, WholesalePrice, RoyaltyQuantity, PrintCost, ExcRateFromGBP from RoyaltyItems"
            self.RoyaltyItemsWindow.SelectedRow = self.RoyaltyItemsWindow.table.currentRow()
            if self.RoyaltyItemsWindow.SelectedRow != -1:
                self.Selection = True
                with sqlite3.connect("PP.db") as db:
                    cursor = db.cursor() #fetching data from database for the edit window
                    sql = "select RoyaltiesID, ISBN, Currency, RoyaltyDiscount, WholesalePrice, RoyaltyQuantity, PrintCost, ExcRateFromGBP from RoyaltyItems where RoyaltyItemsID = {}".format(self.RoyaltyItemsWindow.table.item(self.RoyaltyItemsWindow.SelectedRow, 0).text())
                    cursor.execute(sql)
                    self.EditWindow.originalItemList = list(cursor.fetchone())

        self.EditWindow.Editing = True

        if self.Selection == True: #initialising the edit window
            self.EditWindow.btnConfirm.clicked.connect(self.EditWindow.Validate)
            if self.CurrentTable in ["RoyaltyItems", "BookInvoiceItems"]:
                self.EditWindow.btnConfirm.clicked.connect(self.EditWindow.CheckCalculated)
            else:
                self.EditWindow.btnConfirm.clicked.connect(self.VerifyUpdate)
            self.EditWindow.AddType = self.CurrentTable
            self.EditWindow.selectedID = self.SelectedID
            self.EditWindow.CalendarWidget = dbCalendarWidget()
            self.EditWindow.CalendarWidget.Calendar()
            self.EditWindow.initAddItemWindow()


        
    def VerifyCustomerUpdate(self):
        self.UpdateEntryWindow.Verify = dbConfirmationDialog()
        #new instance for customer verification

        

    def VerifyUpdate(self): #verification dialog
        if self.EditWindow.ReadyToVerify == True:
            self.EditWindow.Verify = dbConfirmationDialog()
            self.EditWindow.Verify.Msg = "Insert Password to confirm all changes"
            self.EditWindow.Verify.ConfirmedMsg = "Update successful"
            self.EditWindow.Verify.VerifyDlg()
            if self.EditWindow.Verify.ConfirmedDialog.Accepted == True:
                self.UpdateChanges()
                self.EditWindow.accept()
            

 
    def UpdateChanges(self): #committing changes
        self.UpdateList = []

        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            if self.CurrentTable == "Book":
                self.NoOfEntries = 12
                cursor.execute("select * from Book")
                self.ID = "ISBN"
                self.SelectedISBN = QTableWidgetItem(self.ViewWindow.table.item(self.ViewWindow.SelectedRow, 0)).text()
                self.SelectedID = self.SelectedISBN
                self.BookEdited = True

            elif self.CurrentTable == "PubInvoice":
                cursor.execute("select ISBN, AuthorID, PubInvoiceDate, PubInvoiceService, PubInvoicePayment from PubInvoice")
                self.NoOfEntries = 5
                self.ID = "PubInvoiceID"
                self.SelectedID = QTableWidgetItem(self.PubInvoiceWindow.table.item(self.PubInvoiceWindow.SelectedRow, 0)).text()

            elif self.CurrentTable == "BookInvoice":
                cursor.execute("select AuthorID, BookInvoiceDate from BookInvoice")
                self.NoOfEntries = 2
                self.ID = "BookInvoiceID"
                self.SelectedID = QTableWidgetItem(self.BookInvoiceWindow.table.item(self.BookInvoiceWindow.SelectedRow, 0)).text()

            elif self.CurrentTable == "Royalties":
                cursor.execute("select AuthorID, RoyaltiesDate from Royalties")
                self.NoOfEntries = 2
                self.ID = "RoyaltiesID"
                self.SelectedID = QTableWidgetItem(self.RoyaltiesWindow.table.item(self.RoyaltiesWindow.SelectedRow, 0)).text()
                
            elif self.CurrentTable == "BookInvoiceItems":
                cursor.execute("select BookInvoiceID, ISBN, BookInvoiceQuantity, BookInvoiceDiscount, ShippingType, ShippingPrice from BookInvoiceItems")
                self.NoOfEntries = 6
                self.ID = "BookInvoiceItemsID"
                self.SelectedID = QTableWidgetItem(self.BookInvoiceItemsWindow.table.item(self.BookInvoiceItemsWindow.SelectedRow, 0)).text()

            elif self.CurrentTable == "RoyaltyItems":
                cursor.execute("select RoyaltiesID, ISBN, Currency, RoyaltyDiscount, WholesalePrice, RoyaltyQuantity, PrintCost, ExcRateFromGBP from RoyaltyItems")
                self.NoOfEntries = 6
                self.ID = "RoyaltyItemsID"
                self.SelectedID = QTableWidgetItem(self.RoyaltyItemsWindow.table.item(self.RoyaltyItemsWindow.SelectedRow, 0)).text()
        
        for count in range(0, self.NoOfEntries): #creating the update string for sql
            try:
                self.UpdateList.append(str(self.EditWindow.inputList[count].currentText()))
            except:
                if count == 8 and self.AddType == "RoyaltyItems":
                    self.UpdateList.append(str(self.NetSales))
                else:
                    self.UpdateList.append(self.EditWindow.inputList[count].text())
                
        self.Update = ""
                
        self.Headers = list(cursor.description)
        for count in range(0, len(self.UpdateList)):
            self.Update += "{} = '{}'".format(list(self.Headers[count])[0], self.UpdateList[count])
            if count != len(self.UpdateList) - 1:
                self.Update += ", "
                    
        with sqlite3.connect("PP.db") as db: #update
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            if self.CurrentTable == "Book": #ISBN is primary key which may be changed, so all foreign keys will change first for it
                try:
                    sql = "update PubInvoice set ISBN = {0} where ISBN = {1}".format(self.UpdateList[0], self.SelectedID)
                    cursor.execute(sql)
                    sql = "update BookInvoiceItems set ISBN = {0} where ISBN = {1}".format(self.UpdateList[0], self.SelectedID)
                    cursor.execute(sql)
                    sql = "update RoyaltyItems set ISBN = {0} where ISBN = {1}".format(self.UpdateList[0], self.SelectedID)
                    cursor.execute(sql)
                except:
                    pass # error if no entry is there for pubinvoice/bookinvoiceitems/royaltyitems
            sql = "update {} set {} where {} = {}".format(self.CurrentTable, self.Update, self.ID, self.SelectedID)
            cursor.execute(sql)
            db.commit()
            
        self.RefreshTables()
        
        try:
            self.RecalculateItems()
            self.BookEdited = False
        except:
            pass
        


    def RefreshTables(self): #refreshing tables
        if self.CurrentTable == "Customer":
            self.TableWidget.sql = "select * from Customer"
            self.TableWidget.initTable()
            
        if self.CurrentTable == "Book": 
            self.ViewWindow.table.sql = "select * from Book where AuthorID = {}".format(self.SelectedAuthorID)
            self.ViewWindow.table.initTable()
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                cursor.execute("select Firstname, Lastname from Customer where AuthorID = {}".format(self.SelectedAuthorID))
                self.Name = list(cursor.fetchone())
                self.Name = "{}, {}".format(self.Name[1], self.Name[0])
                for count in range(0, self.TableWidget.rowCount()+1):
                    self.ViewWindow.table.setItem(count, 1, QTableWidgetItem(self.Name))
                self.ViewWindow.table.setHorizontalHeaderItem(1, QTableWidgetItem("Author"))
                
        elif self.CurrentTable == "PubInvoice":
            self.PubInvoiceWindow.table.sql = "select * from PubInvoice where ISBN = {}".format(self.SelectedISBN)
            self.PubInvoiceWindow.table.initTable()
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                cursor.execute("select BookTitle from Book where ISBN = {}".format(self.SelectedISBN))
                self.Title = "{}".format(list(cursor.fetchone())[0])
                for count in range(0, self.TableWidget.rowCount()+1):
                    self.PubInvoiceWindow.table.setItem(count, 1, QTableWidgetItem(self.Title))
                self.PubInvoiceWindow.table.setHorizontalHeaderItem(1, QTableWidgetItem("BookTitle"))
                cursor.execute("select Firstname, Lastname from Customer where AuthorID = {}".format(self.SelectedAuthorID))
                self.Name = list(cursor.fetchone())
                self.Name = "{}, {}".format(self.Name[1], self.Name[0])
                for count in range(0, self.TableWidget.rowCount()+1):
                    self.PubInvoiceWindow.table.setItem(count, 2, QTableWidgetItem(self.Name))
                self.PubInvoiceWindow.table.setHorizontalHeaderItem(2, QTableWidgetItem("Author"))
            

        elif self.CurrentTable == "BookInvoice":
            self.BookInvoiceWindow.table.sql = "select * from BookInvoice where AuthorID = {}".format(self.SelectedAuthorID)
            self.BookInvoiceWindow.table.initTable()
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                cursor.execute("select Firstname, Lastname from Customer where AuthorID = {}".format(self.SelectedAuthorID))
                self.Name = list(cursor.fetchone())
                self.Name = "{}, {}".format(self.Name[1], self.Name[0])
                for count in range(0, self.TableWidget.rowCount()+1):
                    self.BookInvoiceWindow.table.setItem(count, 1, QTableWidgetItem(self.Name))
                self.BookInvoiceWindow.table.setHorizontalHeaderItem(1, QTableWidgetItem("Author"))
            

        elif self.CurrentTable == "Royalties":
            self.RoyaltiesWindow.table.sql = "select * from Royalties where AuthorID = {}".format(self.SelectedAuthorID)
            self.RoyaltiesWindow.table.initTable()
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                cursor.execute("select Firstname, Lastname from Customer where AuthorID = {}".format(self.SelectedAuthorID))
                self.Name = list(cursor.fetchone())
                self.Name = "{}, {}".format(self.Name[1], self.Name[0])
                for count in range(0, self.TableWidget.rowCount()+1):
                    self.RoyaltiesWindow.table.setItem(count, 1, QTableWidgetItem(self.Name))
                self.RoyaltiesWindow.table.setHorizontalHeaderItem(1, QTableWidgetItem("Author"))
            
        elif self.CurrentTable == "BookInvoiceItems":
            self.BookInvoiceItemsWindow.table.sql = "select * from BookInvoiceItems where BookInvoiceID = {}".format(self.SelectedID)
            self.BookInvoiceItemsWindow.table.initTable()
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                self.ID = []
                sql = "select BookInvoiceItemsID from BookInvoiceItems where BookInvoiceID = {}".format(self.SelectedID)
                cursor.execute(sql)
                self.IDList = list(cursor.fetchall())
                for count in range(0, len(self.IDList)):
                    self.temp = list(self.IDList[count])[0]
                    self.ID.append(self.temp)
                                   
                for count in range(0, len(self.ID)):
                    try:
                        cursor.execute("select Book.BookTitle, BookInvoiceItems.ISBN from Book, BookInvoiceItems where BookInvoiceItems.BookInvoiceID = {} and BookInvoiceItems.BookInvoiceItemsID = {} and Book.ISBN = BookInvoiceItems.ISBN".format(self.SelectedID, self.ID[count]))
                        self.Title = list(cursor.fetchone())[0]
                        self.BookInvoiceItemsWindow.table.setItem(count, 2, QTableWidgetItem(str(self.Title)))
                    except:
                        pass
                self.BookInvoiceItemsWindow.table.setHorizontalHeaderItem(0, QTableWidgetItem("BookTitle"))
                self.BookInvoiceItemsWindow.table.removeColumn(1)
                
        elif self.CurrentTable == "RoyaltyItems":
            self.RoyaltyItemsWindow.table.sql = "select * from RoyaltyItems where RoyaltiesID = {}".format(self.SelectedID)
            self.RoyaltyItemsWindow.table.initTable()
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                self.ID = []
                sql = "select RoyaltyItemsID from RoyaltyItems where RoyaltiesID = {}".format(self.SelectedID)
                cursor.execute(sql)
                self.IDList = list(cursor.fetchall())
                for count in range(0, len(self.IDList)):
                    self.temp = list(self.IDList[count])[0]
                    self.ID.append(self.temp)
                                   
                for count in range(0, len(self.ID)):
                    try:
                        cursor.execute("select Book.BookTitle, RoyaltyItems.ISBN from Book, RoyaltyItems where RoyaltyItems.RoyaltiesID = {} and RoyaltyItems.RoyaltyItemsID = {} and Book.ISBN = RoyaltyItems.ISBN".format(self.SelectedID, self.ID[count]))
                        self.Title = list(cursor.fetchone())[0]
                        self.RoyaltyItemsWindow.table.setItem(count, 2, QTableWidgetItem(str(self.Title)))
                    except:
                        pass
                self.RoyaltyItemsWindow.table.setHorizontalHeaderItem(0, QTableWidgetItem("BookTitle"))
                self.RoyaltyItemsWindow.table.removeColumn(1)


    def Back(self): #going back from the view window to the main menu
        self.ViewWindow.table.selectedID = None 
        self.CurrentTable = "Customer"
        self.StackedLayout.setCurrentIndex(0)
        self.MenuBar.setVisible(True)



    def QuickSearch(self): #quick search from main menu
        self.QSText = self.MainMenuButtons.leQuickSearch.text()
        self.QSText = self.QSText.split(' ')
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            
            if len(self.QSText) == 1:
                self.TableWidget.sql = "select * from Customer where Firstname like '{0}%' or Lastname like '{0}%'".format(self.QSText[0])
            elif len(self.QSText) == 0:
                self.TableWidget.sql = "select * from Customer"
            else:
                for count in range(1, len(self.QSText)):
                    if count != 1:
                        self.QSText[1] += " {}".format(self.QSText[count])
                self.TableWidget.sql = "select * from Customer where Firstname like '{0}%' and Lastname like '{1}%'".format(self.QSText[0], self.QSText[1])
            self.TableWidget.initTable()



    def Search(self): #main search interface
        self.SearchDatabase = dbSearchDatabase()
        self.SearchDatabase.Table = None
        self.SearchDatabase.Valid = False
        self.SearchDatabase.CalendarWidget = dbCalendarWidget()
        self.SearchDatabase.CalendarWidget.Calendar()
        self.SearchDatabase.initLayout()
        if self.SearchDatabase.Valid == True:
            if self.SearchDatabase.Table != None:
                try:
                    if self.SearchDatabase.Table == "Book":
                        for count in range(2, len(list(self.SearchDatabase.Results)[0])):
                            try:
                                if count == 2:
                                    self.SearchTable.sql = "select * from {} where ISBN = '{}'".format(self.SearchDatabase.Table, list(self.SearchDatabase.Results[0])[count])
                                else:
                                    self.SearchTable.sql += " or ISBN = '{}'".format(list(self.SearchDatabase.Results[count - 2])[2])
                                self.SearchTable.initTable()
                            except IndexError:
                                self.SearchTable.initTable()

                    if self.SearchDatabase.Table in ["RoyaltyItems", "BookInvoiceItems"]:
                        start = 4
                    else:
                        start = 1
                        
                    if self.SearchDatabase.Table == "Customer":
                        start = 0
                        for count in range(start, (len(list(self.SearchDatabase.Results)[0]) * len(self.SearchDatabase.Results))):
                            try:
                                if count == start:
                                    self.SearchTable.sql = "select * from Customer where AuthorID = '{}'".format(list(self.SearchDatabase.Results[0])[count])
                                else:
                                    self.SearchTable.sql += " or AuthorID = '{}'".format(list(self.SearchDatabase.Results[count])[0])
                                self.SearchTable.initTable()
                                
                            except IndexError:
                                self.SearchTable.initTable()
                    
                    elif self.SearchDatabase.Table != "Book" and self.SearchDatabase.Table != None:
                        for count in range(start, (len(list(self.SearchDatabase.Results)[0]) * len(self.SearchDatabase.Results))):
                            try:
                                if count == start:
                                    self.SearchTable.sql = "select * from {0} where {0}ID = '{1}'".format(self.SearchDatabase.Table, list(self.SearchDatabase.Results[0])[count])
                                else:
                                    self.SearchTable.sql += " or {0}ID = '{1}'".format(self.SearchDatabase.Table, list(self.SearchDatabase.Results[count-4])[4])
                                self.SearchTable.initTable()
                                
                            except IndexError:
                                self.SearchTable.initTable()


                    self.StackedLayout.setCurrentIndex(2)
                    self.MenuBar.setVisible(False)
                    
                except IndexError:
                    self.Msg = QMessageBox()
                    self.Msg.setWindowTitle("No Results Found")
                    self.Msg.setText("No data matches your search")
                    self.Msg.exec_()


    def keyReleaseEvent(self, QKeyEvent):
        if self.MainMenuButtons.leQuickSearch.text() == "":
            self.TableWidget.sql = "select * from Customer"
            self.TableWidget.initTable()


    def ChangeUsernameOrPassword(self):

        self.ChangeWhat = dbUsernameOrPassword()
        self.ChangeWhat.Selection = None
        self.ChangeWhat.ChangeSelection()
        if self.ChangeWhat.Selection == "Username":
            self.UsernameChange = dbChangeUsername()
            self.UsernameChange.Username = self.Username
            self.UsernameChange.initChangeUsernameScreen()
        elif self.ChangeWhat.Selection == "Password":
            self.PasswordChange = dbChangePassword()
            self.PasswordChange.Username = self.Username
            self.PasswordChange.initChangePasswordScreen()

    def LogOut(self):
        self.hide()
        subprocess.call("LoginDB.py", shell=True)


