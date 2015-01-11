from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
from MenuBar import *
from initMainMenuButtons import *
from AddEntryWindow import *
from TableWidget import *
from ConfirmationDialog import *

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

        #connections
        self.MenuBar.refresh.triggered.connect(self.RefreshTable) 
        self.MainMenuButtons.btnAddEntry.clicked.connect(self.AddEntryWindow.initAddEntryWindow) #connection for 'add entry'
        self.MainMenuButtons.btnRemoveEntry.clicked.connect(self.RemoveEntry)
        
    def RefreshTable(self): #refreshing table to show changes made
        self.TableWidget.CustomerTable()


    def RemoveEntry(self):
        self.SelectedRow = self.TableWidget.currentRow()
        self.SelectedAuthorID = QTableWidgetItem(self.TableWidget.item(self.SelectedRow, 0)).text()
        
        self.ConfirmDialog = ConfirmationDialog()
        self.ConfirmDialog.RemoveDlg()
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys_ = ON")
            sql = "delete from Customer where AuthorID = {}".format(self.SelectedAuthorID)
            cursor.execute(sql)
            db.commit()
        
def main():
    app = QApplication(sys.argv)
    launcher = MainWindow()
    launcher.raise_()
    launcher.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
