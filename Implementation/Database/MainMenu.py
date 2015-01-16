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
from AddBookWindow import *

class MainWindow(QMainWindow):
    """main window"""

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Main Menu")
        self.setFixedSize(735,400)
        self.MenuBar = dbMenuBar()
        self.setMenuBar(self.MenuBar)
        
        self.TableWidget = dbTableWidget()
        self.TableWidget.currentTable = "Customer"
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
        self.ViewWindow.table.currentTable = "Book"
        self.ViewWindow.vertical.addWidget(self.ViewWindow.table)
        self.ViewWindow.vertical.addLayout(self.ViewWindow.horizontalBottom)
        self.ViewWindow.setLayout(self.ViewWindow.vertical)
        
        self.StackedLayout.addWidget(self.ViewWindow)
        
        #connections
        self.MainMenuButtons.btnAddEntry.clicked.connect(self.AddEntry) #connection for 'add entry'
        self.MainMenuButtons.btnRemoveEntry.clicked.connect(self.RemoveEntry) #connection for 'remove entry'
        self.MainMenuButtons.btnView.clicked.connect(self.ViewCustomer)
        self.ViewWindow.btnBack.clicked.connect(self.Back)
        self.ViewWindow.btnAddBook.clicked.connect(self.AddBookWindow)

    def initLayout(self):

        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            sql = "select * from {}".format(self.currentTable)
            cursor.execute(sql)
        self.columns = [tuple[0] for tuple in cursor.description]
        
    
    def AddBookWindow(self):
        self.AddBookWindow = dbAddBookWindow()
        self.currentTable = "Book"
        self.initLayout()
        #self.AddBookWindow.initAddBookWindow()
       
    def ViewCustomer(self):

        self.ViewWindow.table.selectedID = QTableWidgetItem(self.TableWidget.item(self.TableWidget.currentRow(), 0)).text()

        if self.ViewWindow.table.selectedID != "":
            self.ViewWindow.table.currentTable = "Book"
            self.StackedLayout.setCurrentIndex(1)
            self.ViewWindow.table.BookTable()
            self.MenuBar.setVisible(False)
            
        
    def Back(self):
        self.ViewWindow.table.selectedID = ""
        self.StackedLayout.setCurrentIndex(0)
        self.MenuBar.setVisible(True)
    
    def RefreshTable(self): #refreshing table to show changes made
        self.TableWidget.CustomerTable()

    def AddEntry(self):
        self.AddEntryWindow = dbAddEntryWindow()
        self.AddEntryWindow.initAddEntryWindow()
        self.RefreshTable()

    def RemoveEntry(self): #remove entry
        self.SelectedRow = self.TableWidget.currentRow()
        self.SelectedAuthorID = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 0)).text()
        #getting AuthorID of a row
        self.ConfirmDialog = ConfirmationDialog()
        self.Firstname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 1)).text()
        self.Lastname = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 2)).text()
        self.ConfirmDialog.Name = "{} {}".format(self.Firstname, self.Lastname)
        self.ConfirmDialog.RemoveDlg()
        
        if self.ConfirmDialog.ConfirmedDialog.Accepted == True:
            with sqlite3.connect("PP.db") as db:
                cursor = db.cursor()
                cursor.execute("PRAGMA foreign_keys_ = ON")
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
