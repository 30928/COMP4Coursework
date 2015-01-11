from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class dbMenuBar(QMenuBar):
    """the menu bar"""
    
    def __init__(self):
        super().__init__()

        #self.menu_bar = QMenuBar(self) #creating the menu bar
        
        self.search_database = QAction("Search Database", self) #creating actions
        self.add_entry = QAction("Add Entry", self)
        self.update_entry = QAction("Update Entry", self)
        self.remove_entry = QAction("Remove Entry", self)
        self.refresh = QAction("Refresh Table", self)
        self.change_password = QAction("Change Password", self)
        self.log_out = QAction("Log Out", self)
        
        self.database_menu = self.addMenu("Database") #adding menus
        self.database_menu.addAction(self.search_database) #adding actions to menus
        
        self.actions_menu = self.addMenu("Actions")
        self.actions_menu.addAction(self.add_entry)
        self.actions_menu.addAction(self.update_entry)
        self.actions_menu.addAction(self.remove_entry)
        self.actions_menu.addAction(self.refresh)

        self.account_menu = self.addMenu("Account")
        self.account_menu.addAction(self.change_password)
        self.account_menu.addAction(self.log_out)


        
