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

class MainWindow(QMainWindow):
    """main window"""

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Main Menu")
        self.setFixedSize(735,400)
        self.MenuBar = dbMenuBar()
        self.setMenuBar(self.MenuBar)
        
        self.TableWidget = dbTableWidget()
        self.TableWidget.initTable()
        self.TableWidget.CustomerTable()
        
        self.MainMenuButtons = initMainMenuButtons()
        self.MainMenuButtons.vertical.addLayout(self.MainMenuButtons.horizontalTop)
        self.MainMenuButtons.vertical.addWidget(self.TableWidget)
        self.MainMenuButtons.vertical.addLayout(self.MainMenuButtons.horizontalBottom)
        self.MainMenuButtons.setLayout(self.MainMenuButtons.vertical)
        self.setCentralWidget(self.MainMenuButtons)
        
        self.AddEntryWindow = dbAddEntryWindow()
        #self.ViewWindow = dbViewWindow()
        
        #connections
        self.MainMenuButtons.btnAddEntry.clicked.connect(self.AddEntry) #connection for 'add entry'
        self.MainMenuButtons.btnRemoveEntry.clicked.connect(self.RemoveEntry) #connection for 'remove entry'

        
    def RefreshTable(self): #refreshing table to show changes made
        self.TableWidget.CustomerTable()

    def AddEntry(self):
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
