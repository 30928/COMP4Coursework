from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class dbAddItemWindow(QDialog):
    """add entry window dialog"""

    def __init__(self):
        super().__init__()
    
    def initAddItemWindow(self):
        self.setWindowTitle("Add {}".format(self.AddType))
        self.setFixedSize(350,200)
        self.setModal(True) #modal window
        
        with sqlite3.connect("PP.db") as db: #fetching data from db
            cursor = db.cursor()
            cursor.execute(self.sql)
            db.commit()

            
        self.columns = [tuple[0] for tuple in cursor.description] #column names
        
        places = [(count,count2) for count in range (int(round(len(self.columns)/2,1)+1)) for count2 in range(4)]
        self.columns = sum([[count,''] for count in self.columns],[])
        db.close()
        self.inputList = []
        self.qlabelList = []
        self.gridLayout = QGridLayout()
        count = 0
        for place, self.columnHeader in zip(places, self.columns):

            if self.columnHeader == '': #replacing spaces with line edits

                if self.AddType == "Book" and count == 1: #exceptions for book
                    self.input = QLineEdit(self) #new line edit
                    self.input.setReadOnly(True)
                    self.input.setText(self.selectedID)
                    self.ReadyForLayout = True
        
                elif self.AddType == "Book" and count in [4, 5, 6, 7]: #exceptions for book
                    self.input = QComboBox(self) #new combo box
                    self.ReadyForLayout = True
                    
                elif self.AddType == "PubInvoice" and count == 0:
                    self.ReadyForLayout = False #skips pubinvoiceID
                    oount 
                
                else:
                    self.input = QLineEdit(self) #new line edit #standard input method

                if self.ReadyForLayout == True:
                    self.inputList.append(self.input)   #line edits/combo boxes appended to list for further reference
                    self.gridLayout.addWidget(self.inputList[count], *place)

                count += 1
                
            else: #adding qlabels with the line edits
                if self.AddType == "Book" and count == 10: #adding date button instead of qlabel
                    self.btnDate = QPushButton("Date", self)
                    self.qlabelList.append(self.btnDate)
                else:            
                    self.qlabel = QLabel(str(self.columnHeader), self)
                    self.qlabelList.append(self.qlabel)
                self.gridLayout.addWidget(self.qlabelList[count], *place)

        if self.AddType == "Book":
            self.inputList[4].addItem("Large")
            self.inputList[4].addItem("Small")
            self.inputList[5].addItem("Hard")
            self.inputList[5].addItem("Soft")
            self.inputList[6].addItem("Colour")
            self.inputList[6].addItem("Black/White")
            self.inputList[7].addItem("White")
            self.inputList[7].addItem("Creme")
            
            self.inputList[10].setReadOnly(True)


        self.horizontal = QHBoxLayout()
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnCancel)
        self.horizontal.addWidget(self.btnConfirm)
            
        self.vertical = QVBoxLayout()
        self.vertical.addLayout(self.gridLayout)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
            
        self.btnConfirm.clicked.connect(self.accept) #accept on clicking confirm
        self.btnCancel.clicked.connect(self.reject) #reject on clicking cancel
        self.exec_()
        
    def AnswerButtons(self):
        self.btnConfirm = QPushButton("Confirm", self)
        self.btnCancel = QPushButton("Cancel", self)


        
    
