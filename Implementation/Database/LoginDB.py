from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
import smtplib
import email
from MainMenu import *

class dbLogin(QMainWindow):
    """db for login"""

    def __init__(self):
        self.initDetails()
        if self.details == ("Username", "Password"):
            self.MainProgram = MainWindow("Username")
            self.MainProgram.show()
        else:
            super().__init__()
            self.initLoginScreen()

    def initDetails(self):
        with sqlite3.connect("dbLogin.db") as db:
            cursor = db.cursor()

            self.sql = "select name from sqlite_master WHERE type='table' and name='LoginDetails'"
            cursor.execute(self.sql)
            try:
                self.Exists = list(cursor.fetchone())[0]
            except:
                self.Exists = False
            
            self.sql = "create table if not exists LoginDetails (Username text, Password text)"
            cursor.execute(self.sql)
            
            if self.Exists == False:
                self.details = "Username", "Password"
                self.sql = "insert into LoginDetails (Username, Password) values (?, ?)"
                cursor.execute(self.sql, self.details)
            else:
                self.details = True

    def initLoginScreen(self):
        self.setWindowTitle("Login")
        self.setFixedSize(300, 170)
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
        self.lblForgot = QLabel("Help/Forgotten Password?", self)
        self.lblForgot.setAlignment(Qt.AlignHCenter)
        self.lblForgot.mousePressEvent = self.getEmail
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
        self.vertical.addWidget(self.lblForgot)
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

    def getEmail(self, QMouseEvent):
        with sqlite3.connect("dbLogin.db") as db:
            cursor = db.cursor()
            cursor.execute("select Username from LoginDetails")
            self.Username = list(cursor.fetchone())[0]
            
        if self.Username == "Username":
            self.Msg = QMessageBox()
            self.Msg.setWindowTitle("First Time")
            self.Msg.setText("This is your first time using this application.\n Your Username is 'Username' and your Password is 'Password'.\n Please change these once logged in.")
            self.Msg.exec_()
        else:
            self.Email, ok = QInputDialog.getText(self, 'Forgotten Password', 'Enter your Email:')

            if self.Email == self.Username:
                with sqlite3.connect("dbLogin.db") as db:
                    cursor = db.cursor()
                    cursor.execute("select Password from LoginDetails")
                    self.CurrentPassword = list(cursor.fetchone())[0]
                self.sender = "pp.loginhelp@gmail.com"
                self.recipient = [str(self.Email)]
                self.server = smtplib.SMTP('smtp.gmail.com', 587)
                self.server.ehlo()
                self.server.starttls()
                self.server.ehlo()
                self.server.login("pp.loginhelp@gmail.com", "DB1061NH31P")
                
                self.Subject = "Forgotten Login Details"
                self.message = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n".format(self.sender, ", ".join(self.recipient), self.Subject)
                self.message += "Your Password is: {}\nPlease change this upon login for security reasons.".format(self.CurrentPassword)

                self.server.sendmail(self.sender, self.recipient, self.message)
                self.server.close()               
                
                self.Msg = QMessageBox()
                self.Msg.setWindowTitle("Email Sent")
                self.Msg.setText("You have been sent an email with the corresponding password details")
                self.Msg.exec_()
                
            else:
                
                self.Msg = QMessageBox()
                self.Msg.setWindowTitle("No Match found")
                self.Msg.setText("No matching Email was found")
                self.Msg.exec_()
        
    def keyReleaseEvent(self, QKeyEvent):
        if self.lblInvalid != None:
            self.lblInvalid.hide()

def main():
    app = QApplication(sys.argv)
    launcher = dbLogin()
    try:
        launcher.raise_()
        launcher.show()
    except RuntimeError:
        pass
    app.exec_()



            
if __name__ == "__main__":
    main()
