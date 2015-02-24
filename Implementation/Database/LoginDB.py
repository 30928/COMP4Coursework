from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
import smtplib
import email
import time
from MainMenu import *

class dbLogin(QMainWindow):
    """db for login"""

    def __init__(self):
        self.initSplashScreen()
        self.initDetails()
        if self.details == ("Username", "Password"):
            self.customer_table()
            self.book_table()
            self.pub_invoice_table()
            self.book_invoice_table()
            self.book_invoice_items_table()
            self.royalties_table()
            self.royalty_items_table()
            self.hide()
            self.MainProgram = MainWindow("Username") #runs main window if Username/Password haven't been changed before
            self.MainProgram.show()
        else:
            super().__init__() #runs login screen if they have been changed
            self.setStyleSheet("""QPushButton{
                                    min-height: 1.5em;
                                    min-width: 3em;
                                    font: 14px;
                                    color: black;
                                    background-color: #FFFFFF;
                                    padding: 1px;
                                    border-style: outset;
                                    border-width: 1px;
                                    border-color: #8F8F00;}
                                }""")
            self.initLoginScreen()

    def initDetails(self):
        with sqlite3.connect("dbLogin.db") as db:
            cursor = db.cursor()

            self.sql = "select name from sqlite_master WHERE type='table' and name='LoginDetails'"
            cursor.execute(self.sql) #checking whether the login table exists
            try:
                self.Exists = list(cursor.fetchone())[0]
            except:
                self.Exists = False
            
            self.sql = "create table if not exists LoginDetails (Username text, Password text)"
            cursor.execute(self.sql) #creates login table if it doesn't exist
            
            if self.Exists == False: 
                self.details = "Username", "Password"
                self.sql = "insert into LoginDetails (Username, Password) values (?, ?)"
                cursor.execute(self.sql, self.details) #adds default Username and Password
            else:
                self.details = True

    def initLoginScreen(self):
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("LoginIcon.png"))
        self.setFixedSize(300, 190)
        self.lblLogin = QLabel("Please Log In", self)
        self.lblLogin.setFont(QFont("Calibri",14))
        self.lblLogin.setAlignment(Qt.AlignHCenter)
        self.btnLogin = QPushButton("Login", self)
        self.btnLogin.setFixedSize(self.btnLogin.sizeHint())
        self.lblUsername = QLabel("Username:", self)
        self.lblUsername.setFont(QFont("Calibri", 10))
        self.lblPassword = QLabel("Password:", self)
        self.lblPassword.setFont(QFont("Calibri", 10))
        self.leUsername = QLineEdit(self)
        self.leUsername.setPlaceholderText("Username")
        self.lePassword = QLineEdit(self)
        self.lePassword.setEchoMode(self.lePassword.Password)
        self.lePassword.setPlaceholderText("Password")
        self.lblForgot = QLabel("Help/Forgotten Password?", self)
        self.Underline = QFont("Calibri", 10)
        self.Underline.setUnderline(True)
        self.lblForgot.setFont(self.Underline)
        #self.lblLogin.setFont(QFont("Calibri",10))
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
            self.Username = list(cursor.fetchall()) #fetches original username and password
            cursor.execute("select Password from LoginDetails")
            self.Password = list(cursor.fetchall())
            self.Valid = False
            
            for count in range(0, len(self.Username)):
                if self.leUsername.text().lower() == list(self.Username[count])[0].lower():
                    if self.lePassword.text() == list(self.Password[count])[0]:
                        self.Valid = True
                        self.customer_table() #checking all tables to see if they're existent
                        self.book_table()
                        self.pub_invoice_table()
                        self.book_invoice_table()
                        self.book_invoice_items_table()
                        self.royalties_table()
                        self.royalty_items_table()
                        self.hide() #Username and password match, so the user is logged in
                        self.MainProgram = MainWindow(list(self.Username[count])[0])
                        self.MainProgram.show()
                        break
                else:
                    self.Valid = False
                    
            if self.Valid == False:
                if self.lblInvalid == None: #Username and password do not match, user is rejected
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
            cursor.execute("select Password from LoginDetails")
            self.Password = list(cursor.fetchone())[0]
            
        if self.Username == "Username" and self.Password == "Password":
            self.Msg = QMessageBox()
            self.Msg.setWindowTitle("First Time")
            self.Msg.setText("This is your first time using this application.\n Your Username is 'Username' and your Password is 'Password'.\n Please change these once logged in.")
            self.Msg.exec_() #default username and password is shown to the user
        else:
            self.Email, ok = QInputDialog.getText(self, 'Forgotten Password', 'Enter your Email:')
            self.Email = self.Email.lower() #email is received from the user
            if self.Email == self.Username:
                with sqlite3.connect("dbLogin.db") as db:
                    cursor = db.cursor()
                    cursor.execute("select Password from LoginDetails")
                    self.CurrentPassword = list(cursor.fetchone())[0] #gets password from database
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
                self.Msg.setWindowTitle("Email Sent") #email is sent if email is existent in the database, with password details
                self.Msg.setText("You have been sent an email with the corresponding password details")
                self.Msg.exec_()
                
            elif self.Email != self.Username and ok == True:
                self.Msg = QMessageBox()
                self.Msg.setWindowTitle("No Match found") #email is not found, so email is not sent
                self.Msg.setText("No matching Email was found")
                self.Msg.exec_()
        
    def keyReleaseEvent(self, QKeyEvent):
        if self.lblInvalid != None:
            self.lblInvalid.hide()

    def create_table(self):
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            self.Exists = True
            self.FindTable = "select name from sqlite_master WHERE type='table' and name='{}'".format(self.TableName)
            cursor.execute(self.FindTable) #checks if the tables exist
            try:
                self.Exists = list(cursor.fetchone())
            except:
                self.Exists = False
                
            if self.Exists == False: #creates tables for the database if they don't already exist
                cursor.execute(self.sql)
                db.commit()

    def customer_table(self):
        self.sql = """create table Customer 
                 (AuthorID integer,
                 FirstName text,
                 LastName text,
                 Email text,
                 PhoneNumber text,
                 Address text,
                 Postcode text,
                 primary key(AuthorID))"""
        self.TableName = "Customer"
        self.create_table()
            
    def book_table(self):
        self.sql = """create table Book 
                 (ISBN text,
                 AuthorID integer,
                 BookTitle text,
                 NoOfPages integer,
                 Size text,
                 Back text,
                 Cover text,
                 Paper text,
                 Font text,
                 FontSize real,
                 DatePublished date,
                 Price real,
                 primary key(ISBN),
                 foreign key(AuthorID) references Customer(AuthorID))"""
        self.TableName = "Book"
        self.create_table()

    def pub_invoice_table(self):
        self.sql = """create table PubInvoice 
                 (PubInvoiceID integer,
                 ISBN text,
                 AuthorID integer,
                 PubInvoiceDate date,
                 PubInvoiceService text,
                 PubInvoicePayment real,
                 primary key(PubInvoiceID),
                 foreign key(AuthorID) references Customer(AuthorID),
                 foreign key(ISBN) references Book(ISBN))"""
        self.TableName = "PubInvoice"
        self.create_table()

    def book_invoice_table(self):
        self.sql = """create table BookInvoice
                 (BookInvoiceID integer,
                 AuthorID integer,
                 BookInvoiceDate date,
                 BookInvoicePayment real,
                 primary key(BookInvoiceID),
                 foreign key(AuthorID) references Customer(AuthorID))"""
        self.TableName = "BookInvoice"
        self.create_table()

    def book_invoice_items_table(self):
        self.sql = """create table BookInvoiceItems
                 (BookInvoiceItemsID integer,
                 BookInvoiceID integer,
                 ISBN text,
                 BookInvoiceQuantity integer,
                 BookInvoiceDiscount real,
                 ShippingType text,
                 ShippingPrice real,
                 primary key(BookInvoiceItemsID),
                 foreign key(BookInvoiceID) references BookInvoice(BookInvoiceID),
                 foreign key(ISBN) references Book(ISBN))"""
        self.TableName = "BookInvoiceItems"
        self.create_table()

    def royalties_table(self):
        self.sql = """create table Royalties
                 (RoyaltiesID integer,
                 AuthorID integer,
                 RoyaltiesDate date,
                 RoyaltyPayment real,
                 primary key(RoyaltiesID),
                 foreign key(AuthorID) references Customer(AuthorID))"""
        self.TableName = "Royalties"
        self.create_table()

    def royalty_items_table(self):
        self.sql = """create table RoyaltyItems
                 (RoyaltyItemsID integer,
                 RoyaltiesID integer,
                 ISBN text,
                 Currency text,
                 RoyaltyDiscount real,
                 WholesalePrice real,
                 RoyaltyQuantity integer,
                 NetSales real,
                 PrintCost real,
                 ExcRateFromGBP real,
                 primary key(RoyaltyItemsID),
                 foreign key(RoyaltiesID) references Royalties(RoyaltiesID),
                 foreign key(ISBN) references Book(ISBN))"""
        self.TableName = "RoyaltyItems"
        self.create_table()
        
    def initSplashScreen(self):
        self.pixmap = QPixmap("PerfectPublishersLtd.png")
        self.Splashscreen = QSplashScreen(self.pixmap, Qt.WindowStaysOnTopHint)
        self.Splashscreen.setMask(self.pixmap.mask())
        self.Splashscreen.show()
        time.sleep(2)
        self.Splashscreen.finish(self.Splashscreen)


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
