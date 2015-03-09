from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbChangeUsername(QDialog):
    """Change Username confirmation"""

    def __init__(self):
        super().__init__()

    def initChangeUsernameScreen(self):
        self.setWindowTitle("Change Username")
        self.setModal(True)
        self.leOldUsername = QLineEdit(self)
        self.leNewUsername = QLineEdit(self)
        self.leNewUsername.setValidator(QRegExpValidator(QRegExp("^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")))
        self.leOldUsername.setValidator(QRegExpValidator(QRegExp("^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")))
        #reg ex from www.regexlib.com
        self.leRetype = QLineEdit(self)
        self.lblOld = QLabel("Old Username:", self)
        self.lblNew = QLabel("New Username:", self)
        self.lblRetype = QLabel("Retype New Username:", self)
        self.leOldUsername.setPlaceholderText("Old Username")
        self.leNewUsername.setPlaceholderText("New Username")
        self.leRetype.setPlaceholderText("Retype New Username")
        self.btnConfirm = QPushButton("Confirm")
        self.btnCancel = QPushButton("Cancel")
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.btnCancel)
        self.horizontal.addWidget(self.btnConfirm)
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.lblOld, 0, 0)
        self.gridLayout.addWidget(self.lblNew, 1, 0)
        self.gridLayout.addWidget(self.lblRetype, 2, 0)
        self.gridLayout.addWidget(self.leOldUsername, 0, 1)
        self.gridLayout.addWidget(self.leNewUsername, 1, 1)
        self.gridLayout.addWidget(self.leRetype, 2, 1)
        self.gridLayout.addLayout(self.horizontal, 3, 2)
        self.setLayout(self.gridLayout)
        self.btnCancel.clicked.connect(self.reject)
        self.btnConfirm.clicked.connect(self.Check)
        self.exec_()
        
    def Check(self):
        if self.leNewUsername.text() == self.leRetype.text():
            
            if len(self.leNewUsername.text()) < 5:
                self.Msg = QMessageBox()
                self.Msg.setWindowTitle("Username")
                self.Msg.setText("New Username was too short")
                self.Msg.exec_()
            else:
                
                with sqlite3.connect("dbLogin.db") as db:
                    cursor = db.cursor()
                    cursor.execute("select Username from LoginDetails")
                    self.OldUsername = list(cursor.fetchone())[0]
                    if self.leOldUsername.text() == self.OldUsername:
                        self.NewUsername = self.leNewUsername.text()
                        cursor.execute("update LoginDetails set Username = '{}' where Username = '{}'".format(self.NewUsername, self.Username))
                        self.Msg = QMessageBox()
                        self.Msg.setWindowTitle("Username")
                        self.Msg.setText("Username was successfully changed")
                        self.Msg.exec_()
                        self.accept()

                    else:
                        self.Msg = QMessageBox()
                        self.Msg.setWindowTitle("Username")
                        self.Msg.setText("Old Username was incorrect")
                        self.Msg.exec_()
        else:
            self.Msg = QMessageBox()
            self.Msg.setWindowTitle("Username")
            self.Msg.setText("New Usernames did not match")
            self.Msg.exec_()

