from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class ToolAndMenuBar(QMainWindow):
    """the tool bar and menu bar"""
    
    def __init__(self):
        super().__init__()

    def MenuBar(self):
        self.menu_bar = QMenuBar(self)
        self.search_database = QAction("Search Database", self)
        self.add_entry = QAction("Add Entry", self)
        self.update_entry = QAction("Update Entry", self)
        self.remove_entry = QAction("Remove Entry", self)
        self.change_password = QAction("Change Password", self)
        self.log_out = QAction("Log Out", self)
        self.database_menu = self.menu_bar.addMenu("Database")
        self.database_menu.addAction(self.search_database)
        self.actions_menu = self.menu_bar.addMenu("Actions")
        self.actions_menu.addAction(self.add_entry)
        self.actions_menu.addAction(self.update_entry)
        self.actions_menu.addAction(self.remove_entry)

        self.account_menu = self.menu_bar.addMenu("Account")
        self.account_menu.addAction(self.change_password)
        
        self.account_menu.addAction(self.log_out)
        self.setMenuBar(self.menu_bar)


        
