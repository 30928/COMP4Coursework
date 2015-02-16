from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbUsernameOrPassword(QDialog):
    """main window"""

    def __init__(self):
        super().__init__()
        
    def ChangeSelection(self):
        self.setModal(True)
        self.setFixedSize(400, 50)
        self.setWindowTitle("Selection")
        self.btnUsername = QPushButton("Change Username", self)
        self.btnPassword = QPushButton("Change Password", self)
        self.btnCancel = QPushButton("Cancel", self)
        self.btnCancel.clicked.connect(self.reject)
        self.btnUsername.clicked.connect(self.UsernameSelected)
        self.btnPassword.clicked.connect(self.PasswordSelected)
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.btnUsername, 0, 0)
        self.gridLayout.addWidget(self.btnPassword, 0, 1)
        self.gridLayout.addWidget(self.btnCancel, 0, 2)
        self.setLayout(self.gridLayout)
        self.exec_()
        
    def UsernameSelected(self):
        self.Selection = "Username"
        self.accept()

    def PasswordSelected(self):
        self.Selection = "Password"
        self.accept()
