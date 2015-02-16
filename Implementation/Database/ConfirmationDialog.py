from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbConfirmationDialog(QDialog):
    """creating confirmation modal dialogs"""

    def __init__(self):
        super().__init__()
        
    def VerifyDlg(self):
        self.setWindowTitle("Verification")
        self.setFixedSize(275, 150)
        self.setModal(True)

        self.lblWarningMsg = QLabel(self.Msg, self)
        self.horizontal = QHBoxLayout()
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.lblWarningMsg)
        self.horizontal.addStretch(1)
        self.lblWarningMsg.setFixedSize(250,30)
        self.lblWarningMsg.setWordWrap(True)
        self.lblWarningMsg.setAlignment(Qt.AlignHCenter)
        
        self.qlePasswordBox = QLineEdit(self)
        self.qlePasswordBox.setFixedSize(100, 25)
        self.qlePasswordBox.setEchoMode(self.qlePasswordBox.Password)
        self.lblPassword = QLabel("Password: ", self)
        
        self.horizontal1 = QHBoxLayout()
        self.horizontal1.addStretch(1)
        self.horizontal1.addWidget(self.lblPassword)
        self.horizontal1.addWidget(self.qlePasswordBox)
        self.horizontal1.addStretch(1)

        self.btnConfirm = QPushButton("Confirm", self)
        self.btnCancel = QPushButton("Cancel", self)
        self.horizontal2 = QHBoxLayout()
        self.horizontal2.addWidget(self.btnCancel)
        self.horizontal2.addWidget(self.btnConfirm)

        self.vertical = QVBoxLayout()
        self.vertical.addLayout(self.horizontal)
        self.vertical.addLayout(self.horizontal1)
        self.vertical.addLayout(self.horizontal2)
        self.vertical.addStretch(1)
        self.setLayout(self.vertical)
        

        self.btnCancel.clicked.connect(self.reject)
        self.ConfirmedDialog = dbConfirmationDialog()
        self.ConfirmedDialog.ConfirmedMsg = self.ConfirmedMsg
        self.lblInvalid = None
        self.btnConfirm.clicked.connect(self.PasswordCheck)                
        
        self.ConfirmedDialog.Accepted = False
        self.exec_()

        
    def PasswordCheck(self):
        with sqlite3.connect("dbLogin.db") as db:
            cursor = db.cursor()
            cursor.execute("select Password from LoginDetails")
            self.Password = list(cursor.fetchall())
            self.Valid = False
            
            for count in range(0, len(self.Password)):
                if self.qlePasswordBox.text() == list(self.Password[count])[0]:
                    self.accept()
                    self.ConfirmedDialog.Confirmed()
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

                    
    def Confirmed(self):
        self.setWindowTitle("Confirmation")
        self.setFixedSize(275, 100)
        self.setModal(True)
        
        self.lblConfirmed = QLabel(self.ConfirmedMsg, self)
        self.lblConfirmed.setFixedSize(250, 50)
        self.lblConfirmed.setWordWrap(True)
        self.lblConfirmed.setAlignment(Qt.AlignHCenter)
        
        self.btnOk = QPushButton("OK", self)
        self.btnOk.setFixedSize(75, 30)
        self.btnOk.clicked.connect(self.accept)
        
        self.horizontal = QHBoxLayout()
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnOk)
        self.horizontal.addStretch(1)
        
        self.vertical = QVBoxLayout()
        self.vertical.addWidget(self.lblConfirmed)
        self.vertical.addStretch(1)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        self.Accepted = True
        self.exec_()

    def keyReleaseEvent(self, QKeyEvent):
        if self.lblInvalid != None:
            self.lblInvalid.hide()

        
