from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbRoyaltiesAndInvoices(QDialog):
    """viewing royalties and invoices"""

    def __init__(self):
        super().__init__()

    def PubInvoice(self):
        self.setWindowTitle("View Publishing Invoices")
        self.setModal(True)
        self.setFixedSize(640, 220)
        self.vertical = QVBoxLayout()
        self.vertical.addWidget(self.table)

        self.btnAddPubInvoice = QPushButton("Add Publishing \n Invoice", self)
        self.btnDeleteEntry = QPushButton("Delete \n Entry", self)
        self.btnAddPubInvoice.setFixedSize(100, 40)
        self.btnDeleteEntry.setFixedSize(100, 40)
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.btnAddPubInvoice)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnDeleteEntry)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        self.exec_()
