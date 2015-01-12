from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
from MainMenu import *

class ConfirmationDialog(QDialog):
    """creating confirmation modal dialogs"""

    def __init__(self):
        super().__init__()
        
    def RemoveDlg(self):
        self.setWindowTitle("Verification")
        self.setFixedSize(275, 100)
        self.setModal(True)

        self.lblWarningMsg = QLabel("Are you sure you want to delete this customer and all records about them?", self)
        self.lblWarningMsg.move(50,50)
        self.lblWarningMsg.setFixedSize(250,50)
        self.lblWarningMsg.setWordWrap(True)
        self.lblWarningMsg.setAlignment(Qt.AlignHCenter)
        
        self.qlePasswordBox = QLineEdit(self)
        self.qlePasswordBox.setFixedSize(100, 25)

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
        self.vertical.addWidget(self.lblWarningMsg)
        self.vertical.addLayout(self.horizontal1)
        self.vertical.addLayout(self.horizontal2)
        self.setLayout(self.vertical)
        
        self.btnConfirm.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.ConfirmedDialog = ConfirmationDialog()
        self.ConfirmedDialog.Name = self.Name
        self.btnConfirm.clicked.connect(self.ConfirmedDialog.Confirmed)
        self.exec_()

    def Confirmed(self):
        self.setWindowTitle("Confirmation")
        self.setFixedSize(275, 100)
        self.setModal(True)
        
        self.lblConfirmed = QLabel("{}'s records have been successfully erased.".format(self.Name), self)
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
        

        
