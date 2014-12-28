from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class MainWindow(QMainWindow):
    """main window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.table = QTableWidget()
        
        #create actions
        self.search_database = QAction("Search Database", self)
        self.add_entry = QAction("Add Entry", self)
        self.update_entry = QAction("Update Entry", self)
        self.remove_entry = QAction("Remove Entry", self)
        self.change_password = QAction("Change Password", self)
        self.log_out = QAction("Log Out", self)
            
        #create menubar and toolbar
        self.menu_bar = QMenuBar()
        self.tool_bar = QToolBar()

        #adding actions to the toolbar
        self.tool_bar.addAction(self.search_database)
        self.tool_bar.addAction(self.add_entry)
        self.tool_bar.addAction(self.update_entry)
        self.tool_bar.addAction(self.remove_entry)
        self.tool_bar.addAction(self.change_password)
        self.tool_bar.addAction(self.log_out)

        #adding actions to the menubar
        self.database_menu = self.menu_bar.addMenu("Database")
        self.database_menu.addAction(self.search_database)

        self.actions_menu = self.menu_bar.addMenu("Actions")
        self.actions_menu.addAction(self.add_entry)
        self.actions_menu.addAction(self.update_entry)
        self.actions_menu.addAction(self.remove_entry)

        self.account_menu = self.menu_bar.addMenu("Account")
        self.account_menu.addAction(self.change_password)
        self.account_menu.addAction(self.log_out)

        #adding the toolbar and menubar to the window
        self.addToolBar(self.tool_bar)
        self.setMenuBar(self.menu_bar)

        self.tool_bar.setMovable(False)

        horizontal = QHBoxLayout()
        self.setLayout(horizontal)

        
        
def main():
    app = QApplication(sys.argv)
    launcher = MainWindow()
    launcher.raise_()
    launcher.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
