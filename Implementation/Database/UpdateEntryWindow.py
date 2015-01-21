from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

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
        self.btnConfirm.clicked.connect(self.accept)
        self.btnConfirm.clicked.connect(self.Verification)
        self.TableName = "Customer"
        self.exec_()

    def Verification(self):
        self.Verify.RemoveDlg()
        
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
            
            self.btnConfirm.clicked.connect.
            self.EditDlg.exec_()

            self.EditInput = self.EditDlg.qle.text()
            self.table.setItem(self.SelectedRow, self.SelectedColumn, QTableWidgetItem(self.EditInput))


    def UpdateChanges(self):
        
        with sqlite3.connect("PP.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "update {} set {} where {} = {}".format(self.TableName, update, ID, data)
            cursor.execute(sql)
            db.commit()
