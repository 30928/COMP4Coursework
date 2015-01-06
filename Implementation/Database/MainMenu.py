from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
from MenuBar import *
from TableWidget import *
from ButtonsAndWindows import *

class MainWindow(QMainWindow):
    """main window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setFixedSize(735,400)
        self.initMenuBar()
        self.initButtonsAndWindows()

        
    def initButtonsAndWindows(self):
        initialiseButtons.Buttons(self)

    def initTable(self):
        TableWidget.initTable(self)
        TableWidget.CustomerTable(self)
        self.vertical.addWidget(self.table)
        
    def initMenuBar(self):
        ToolAndMenuBar.MenuBar(self)
 
def main():
    app = QApplication(sys.argv)
    launcher = MainWindow()
    launcher.raise_()
    launcher.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
