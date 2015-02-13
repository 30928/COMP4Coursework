from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
import os
from MainMenu import *

class dbLogin(QMainWindow):
    """db for login"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)

        self.initLoginScreen()

    def initLoginScreen(self):
        self.lblLogin = QLabel("Please Log In", self)

        self.lblLogin.setAlignment(Qt.AlignHCenter)
        self.btnLogin = QPushButton("Login", self)
        self.btnLogin.setFixedSize(self.btnLogin.sizeHint())
        self.lblUsername = QLabel("Username:", self)
        self.lblPassword = QLabel("Password:", self)
        self.leUsername = QLineEdit(self)
        self.leUsername.setPlaceholderText("Username")
        self.lePassword = QLineEdit(self)
        self.lePassword.setEchoMode(self.lePassword.Password)
        self.lePassword.setPlaceholderText("Password")
        self.lblVertical = QVBoxLayout()
        self.leVertical = QVBoxLayout()
        self.horizontalLogin = QHBoxLayout()
        self.lblVertical.addWidget(self.lblUsername)
        self.leVertical.addWidget(self.leUsername)
        self.lblVertical.addWidget(self.lblPassword)
        self.leVertical.addWidget(self.lePassword)
        self.horizontalLogin.addStretch(1)
        self.horizontalLogin.addWidget(self.btnLogin)
        self.horizontalLogin.addStretch(1)
        self.vertical = QVBoxLayout()
        self.vertical.addWidget(self.lblLogin)
        self.horizontalEntry = QHBoxLayout()
        self.horizontalEntry.addLayout(self.lblVertical)
        self.horizontalEntry.addLayout(self.leVertical)
        self.vertical.addLayout(self.horizontalEntry)
        self.vertical.addLayout(self.horizontalLogin)
        self.vertical.addStretch(1)
        self.horizontal = QHBoxLayout()
        self.horizontal.addStretch(1)
        self.horizontal.addLayout(self.vertical)
        self.horizontal.addStretch(1)
        self.CentralWidget = QWidget()
        self.CentralWidget.setLayout(self.horizontal)
        self.setCentralWidget(self.CentralWidget)
        self.btnLogin.clicked.connect(self.Login)
        self.lblInvalid = None

    def Login(self):
        with sqlite3.connect("dbLogin.db") as db:
            cursor = db.cursor()
            cursor.execute("select Username from LoginDetails")
            self.Username = list(cursor.fetchall())
            cursor.execute("select Password from LoginDetails")
            self.Password = list(cursor.fetchall())
            self.Valid = False
            
            for count in range(0, len(self.Username)):
                if self.leUsername.text() == list(self.Username[count])[0]:
                    if self.lePassword.text() == list(self.Password[count])[0]:
                        self.Valid = True
                        self.MainProgram = MainWindow(list(self.Username[count])[0])
                        self.MainProgram.show()
                        self.hide()
                        break
                else:
                    self.Valid = False
                    
            if self.Valid == False:
                if self.lblInvalid == None:
                    self.lblInvalid = QLabel("Invalid Username or Password - Please try again.", self)
                    self.lblInvalid.setWordWrap(True)
                    self.lblInvalid.setAlignment(Qt.AlignHCenter)
                    self.horizontalInvalid = QHBoxLayout()
                    self.horizontalInvalid.addStretch(1)
                    self.horizontalInvalid.addWidget(self.lblInvalid)
                    self.horizontalInvalid.addStretch(1)
                    self.vertical.addLayout(self.horizontalInvalid)
                else:
                    self.lblInvalid.show()
            
    def keyReleaseEvent(self, QKeyEvent):
        if self.lblInvalid != None:
            self.lblInvalid.hide()

def main():
    app = QApplication(sys.argv)
    launcher = dbLogin()
    launcher.raise_()
    launcher.show()
    app.exec_()



            
if __name__ == "__main__":
    main()
