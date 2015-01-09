from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
from MenuBar import *
from initMainMenuButtons import *
from AddEntryWindow import *
from TableWidget import *

class MainWindow(QMainWindow):
    """main window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setFixedSize(735,400)
        
        self.MenuBar = dbMenuBar()
        self.setMenuBar(self.MenuBar)
        self.TableWidget = dbTableWidget()
        self.TableWidget.
        
        self.MainMenuButtons = initMainMenuButtons()
        self.setCentralWidget(self.MainMenuButtons)
        self.initCustomers()
        self.AddEntryWindow = dbAddEntryWindow()

        self.MenuBar.refresh.triggered.connect(self.RefreshTable) #connections
        self.MainMenuButtons.btnAddEntry.clicked.connect(self.AddEntryWindow.initAddEntryWindow) #connection for 'add entry'

##    def initButtons(self):
##        initMainMenuButtons.Buttons(self)
        
    def initTable(self):
                                    
        self.TableWidget.initTable()
        
    def initCustomers(self):
        

    def RefreshTable(self): #refreshing table to show changes made
        self.initCustomers()

    def RemoveEntry(self):
        pass
        
        
def main():
    app = QApplication(sys.argv)
    launcher = MainWindow()
    launcher.raise_()
    launcher.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
