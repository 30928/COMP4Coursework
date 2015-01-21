from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
from ConfirmationDialog import *

class dbUpdateEntryWindow(QDialog):
    """update entry window dialog"""

    def __init__(self):
        super().__init__()

    def initUpdateEntryWindowDlg(self):
        self.table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setWindowTitle("Update Entry")
        self.setFixedSize(640, 115)
        self.table.setFixedSize(617, 55)
        self.setModal(True)
        self.btnEdit = QPushButton("Edit", self)
        self.btnConfirm = QPushButton("Confirm", self)
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.btnEdit)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnConfirm)
        self.vertical = QVBoxLayout()
        self.vertical.addWidget(self.table)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        self.btnEdit.clicked.connect(self.Edit)
        self.btnConfirm.clicked.connect(self.Verification)
        self.TableName = "Customer"
        self.ID = "AuthorID"
        self.i = 0 #rogue variable
        self.exec_()

    def Verification(self):

        self.Verify.Msg = "Insert Password to confirm all changes"
        self.Verify.ConfirmedMsg = "Update successful"
        
        if self.i == 1:
            self.Verify.open() #NEED TO REINSTANTIATE HERE BUT CAN'T
        if self.i == 0:
            self.i = 1
            self.Verify.VerifyDlg()
        if self.Verify.ConfirmedDialog.Accepted == True:
            self.UpdateChanges()
            self.accept()
        
    def Edit(self):
        self.SelectedItem = self.table.currentItem()
        self.SelectedRow = self.table.currentRow()
        self.SelectedColumn = self.table.currentColumn()
        if self.SelectedItem != None:
            self.EditDlg = dbUpdateEntryWindow()
            self.EditDlg.setModal(True)
            self.EditDlg.setWindowTitle("Input Text")
            self.EditDlg.setFixedSize(210, 120)
            self.EditDlg.lbl = QLabel("Insert text to save over current entry", self)
            self.EditDlg.qle = QLineEdit(self)
            self.EditDlg.qle.setPlaceholderText("Insert text here")
            self.EditDlg.btnConfirm = QPushButton("Confirm", self)
            self.EditDlg.btnConfirm.setFixedSize(60, 25)

            self.EditDlg.qlehorizontal = QHBoxLayout()
            self.EditDlg.btnhorizontal = QHBoxLayout()
            self.EditDlg.qlehorizontal.addStretch(1)
            self.EditDlg.qlehorizontal.addWidget(self.EditDlg.qle)
            self.EditDlg.qlehorizontal.addStretch(1)
            self.EditDlg.btnhorizontal.addStretch(1)
            self.EditDlg.btnhorizontal.addWidget(self.EditDlg.btnConfirm)
            self.EditDlg.btnhorizontal.addStretch(1)
            self.EditDlg.vertical = QVBoxLayout()
            self.EditDlg.vertical.addWidget(self.EditDlg.lbl)
            self.EditDlg.vertical.addLayout(self.EditDlg.qlehorizontal)
            self.EditDlg.vertical.addLayout(self.EditDlg.btnhorizontal)
            self.EditDlg.setLayout(self.EditDlg.vertical)
            self.EditDlg.btnConfirm.clicked.connect(self.EditDlg.accept)
            self.EditDlg.btnConfirm.clicked.connect(self.GetInput)
            self.EditDlg.exec_()
            
    def GetInput(self):
        self.EditInput = self.EditDlg.qle.text()
        self.table.setItem(self.SelectedRow, self.SelectedColumn, QTableWidgetItem(self.EditInput))


    def UpdateChanges(self):
        UL = [] #UL = Update List
        for count in range(0, 6):
            UL.append(self.table.item(0, count).text())
        self.Update = "Firstname = '{}', Lastname = '{}', Email = '{}', Phonenumber = '{}', Address = '{}', Postcode = '{}'".format(UL[0], UL[1], UL[2], UL[3], UL[4], UL[5])
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "update {} set {} where {} = {}".format(self.TableName, self.Update, self.ID, self.SelectedAuthorID)
            cursor.execute(sql)
            db.commit()

