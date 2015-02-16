from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbChangePassword(QDialog):
    """Change password confirmation"""

    def __init__(self):
        super().__init__()

    def initChangePasswordScreen(self):
        self.setModal(True)
        self.leOldPassword = QLineEdit(self)
        self.leNewPassword = QLineEdit(self)
        self.leRetype = QLineEdit(self)
        self.leOldPassword.setEchoMode(self.leOldPassword.Password)
        self.leNewPassword.setEchoMode(self.leNewPassword.Password)
        self.leRetype.setEchoMode(self.leRetype.Password)
        self.lblOld = QLabel("Old Password:", self)
        self.lblNew = QLabel("New Password:", self)
        self.lblRetype = QLabel("Retype New Password:", self)
        self.leOldPassword.setPlaceholderText("Old Password")
        self.leNewPassword.setPlaceholderText("New Password")
        self.leRetype.setPlaceholderText("Retype New Password")
        self.btnConfirm = QPushButton("Confirm")
        self.btnCancel = QPushButton("Cancel")
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.btnCancel)
        self.horizontal.addWidget(self.btnConfirm)
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.lblOld, 0, 0)
        self.gridLayout.addWidget(self.lblNew, 1, 0)
        self.gridLayout.addWidget(self.lblRetype, 2, 0)
        self.gridLayout.addWidget(self.leOldPassword, 0, 1)
        self.gridLayout.addWidget(self.leNewPassword, 1, 1)
        self.gridLayout.addWidget(self.leRetype, 2, 1)
        self.gridLayout.addLayout(self.horizontal, 3, 2)
        self.setLayout(self.gridLayout)

        self.btnCancel.clicked.connect(self.reject)
        self.btnConfirm.clicked.connect(self.Check)
        self.exec_()
        
    def Check(self):
        if self.leNewPassword.text() == self.leRetype.text():
            with sqlite3.connect("dbLogin.db") as db:
                cursor = db.cursor()
                cursor.execute("select Password from LoginDetails")
                self.OldPassword = list(cursor.fetchone())[0]
                if self.leOldPassword.text() == self.OldPassword:
                    self.Password = self.leNewPassword.text()
                    cursor.execute("update LoginDetails set Password = '{}' where Username = '{}'".format(self.Password, self.Username))
                    self.Msg = QMessageBox()
                    self.Msg.setWindowTitle("Password")
                    self.Msg.setText("Password was successfully changed")
                    self.Msg.exec_()
                    self.accept()

                else:
                    self.Msg = QMessageBox()
                    self.Msg.setWindowTitle("Password")
                    self.Msg.setText("Old Password was incorrect")
                    self.Msg.exec_()
        else:
            self.Msg = QMessageBox()
            self.Msg.setWindowTitle("Password")
            self.Msg.setText("New Passwords did not match")
            self.Msg.exec_()
