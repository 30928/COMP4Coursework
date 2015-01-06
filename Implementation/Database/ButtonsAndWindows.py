from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
from TableWidget import *
from MainMenu import *

class initialiseButtons(QMainWindow):
    """initialising buttons and windows"""

    def __init__(self):
        super().__init__()
        
    def Buttons(self):
        self.vertical = QVBoxLayout()


        
        self.btnLogOut = QPushButton("Log Out", QWidget(self))
        self.btnLogOut.setFixedSize(100,30)
        self.leQuickSearch = QLineEdit(QWidget(self))
        self.leQuickSearch.setPlaceholderText("Author Surname")
        self.leQuickSearch.setFixedSize(100,25)
        self.btnQuickSearch = QPushButton("Quick Search", QWidget(self))
        self.btnQuickSearch.setFixedSize(100,30)
                                       
        self.horizontalTop = QHBoxLayout()
        self.horizontalTop.addWidget(self.btnLogOut)
        self.horizontalTop.addStretch(2)
        self.horizontalTop.addWidget(self.leQuickSearch)
        self.horizontalTop.addWidget(self.btnQuickSearch)
        self.vertical.addLayout(self.horizontalTop)
        self.initTable()


        
        self.btnView = QPushButton("View", self)
        self.btnView.setFixedSize(100,40)
        self.btnSearchdb = QPushButton("Search Database", self)
        self.btnSearchdb.setFixedSize(100,40)
        self.btnAddEntry = QPushButton("Add Entry", self)
        self.btnAddEntry.setFixedSize(100,40)
        self.btnUpdateEntry = QPushButton("Update Entry", self)
        self.btnUpdateEntry.setFixedSize(100,40)
        self.btnRemoveEntry = QPushButton("Remove Entry", self)
        self.btnRemoveEntry.setFixedSize(100,40)
        self.btnChangePassword = QPushButton("Change Password", self)
        self.btnChangePassword.setFixedSize(100,40)
    
        self.horizontalBottom = QHBoxLayout()
        self.horizontalBottom.addWidget(self.btnView)
        self.horizontalBottom.addWidget(self.btnSearchdb)
        self.horizontalBottom.addWidget(self.btnAddEntry)
        self.horizontalBottom.addWidget(self.btnUpdateEntry)
        self.horizontalBottom.addWidget(self.btnRemoveEntry)
        self.horizontalBottom.addWidget(self.btnChangePassword)

        
        self.buttons_widget = QWidget()
        self.vertical.addLayout(self.horizontalBottom)
        self.buttons_widget.setLayout(self.vertical)
        self.setCentralWidget(self.buttons_widget)
        self.btnView.clicked.connect(initialiseButtons.ViewWindow)
        self.addEntryDlg = self.btnAddEntry.clicked.connect(initialiseButtons.AddEntry)
        
    def ViewWindow(self, initialiseButtons, TableWidget):
        viewWindowDlg = QDialog()
        viewWindowDlg.setModal(True)
        viewWindowDlg.btnOk = QPushButton("OK", viewWindowDlg)
        viewWindowDlg.exec_()

    def AddEntry(self):
        addEntryDlg = QDialog()
        addEntryDlg.setFixedSize(617,90)
        addEntryDlg.setModal(True)
        addEntryDlg.AddEntryTable = QTableWidget(addEntryDlg)
        addEntryDlg.AddEntryTable.setRowCount(1)
        addEntryDlg.AddEntryTable.setColumnCount(6)
        addEntryDlg.AddEntryTable.setFixedSize(617,55)
        CustomerHeaders = ["Forename", "Surname", "Email", "Phonenumber", "Address", "Postcode"]
        addEntryDlg.AddEntryTable.setHorizontalHeaderLabels(CustomerHeaders)
        addEntryDlg.btnConfirm = QPushButton("Confirm", addEntryDlg)
        addEntryDlg.btnCancel = QPushButton("Cancel", addEntryDlg)
        addEntryDlg.btnConfirm.move(530,60)
        addEntryDlg.btnCancel.move(450, 60)
        addEntryDlg.vertical = QVBoxLayout()
        addEntryDlg.vertical.addWidget(addEntryDlg.AddEntryTable)
        addEntryDlg.btnConfirm.clicked.connect(addEntryDlg.accept)
        addEntryDlg.btnConfirm.clicked.connect(initialiseButtons.adding)
        addEntryDlg.btnCancel.clicked.connect(addEntryDlg.reject)
        addEntryDlg.exec_()
        return addEntryDlg

        addEntryDlg.EntryList = []
        for count in range(0,6):
            item = QTableWidgetItem(addEntryDlg.AddEntryTable.item(0, count)).text()
            addEntryDlg.EntryList.append(item)
            
    def adding(self):
        print(self)
        initialiseButtons.AddEntryToTable(self)

    
    def AddEntryToTable(self, addEntryDlg):
        self.initTable(self)
        self.CustomerTable(self)
        self.table.insertRow(1)
        for count in range(1, 6):
            self.table.setItem(1, count, QTableWidgetItem(str(addEntryDlg.EntryList[count])))
            
            
    
            
    

    




