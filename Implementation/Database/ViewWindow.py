from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbViewWindow(QDialog):
    """view window"""

    def __init__(self):
        super().__init__()

    def ViewDlg(self):
        self.setWindowTitle("Verification")
        self.setFixedSize(735, 400)
        self.setModal(True)

        self.table = QTableWidget(self)
        self.btnViewRoyalties = QPushButton("View Royalties", self)
        self.btnViewBookInvoices = QPushButton("View Book Invoices", self)
        self.btnViewPubInovices = QPushButton("View Publishing Invoice", self)
        self.btnAddBook = QPushButton("Add Book", self)
        self.btnDeleteBook = QPushButton("Delete Book", self)
        self.btn
        self.exec_()
