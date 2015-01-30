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

                if self.AddType == "Book" and count in [1, 4, 5, 6, 7, 10]:

                    if count == 1: #exceptions for book
                        self.input = QLineEdit(self) #new line edit
                        self.input.setReadOnly(True)
                        self.input.setText(self.selectedID)
            
                    elif count in [4, 5, 6, 7]: #exceptions for book where combobox is needed
                        self.input = QComboBox(self) #new combo box

                    elif count == 10:
                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)

                elif self.AddType == "PubInvoice" and count in [0, 1, 2, 3]:
                    
                    if count == 0: #setting  isbn ineditable
                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)
                        self.input.setText(self.selectedISBN)

                    elif count == 1: #setting authorID ineditable
                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)
                        self.input.setText(self.selectedID)

                    elif count == 2:
                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)
                    
                    elif count == 3:
                        self.input = QComboBox(self)
                
                elif self.AddType in ["BookInvoice", "Royalties"] and count in [0, 1]:

                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)
                        
                        if count == 0:
                            self.input.setText(self.selectedID)
                elif self.AddType == "BookInvoiceItems" and count in [0, 1, 4]:

                    if count == 0:
                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)
                        self.input.setText(self.selectedID)
                    elif count == 1:
                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)
                        self.input.setText(self.selectedISBN)
                    elif count == 4:
                        self.input = QComboBox(self)
                        
                else:
                    self.input = QLineEdit(self) #new line edit #standard input method


                self.inputList.append(self.input)   #line edits/combo boxes appended to list for further reference
                self.gridLayout.addWidget(self.inputList[count], *place)

                count += 1
                
            else: #adding qlabels with the line edits
                if self.AddType == "Book" and count == 10: #adding date button instead of qlabel
                    self.btnDate = QPushButton("Date", self)
                    self.qlabelList.append(self.btnDate)
                    self.gridLayout.addWidget(self.qlabelList[count], *place)
                    self.btnDate.clicked.connect(self.CalendarWidget.DisplayCalendar)
                    self.CalendarWidget.btnSelect.clicked.connect(self.getDate)

                elif self.AddType == "PubInvoice" and count == 2: #data button instead of qlabel
                    self.btnDate = QPushButton("Date", self)
                    self.qlabelList.append(self.btnDate)
                    self.gridLayout.addWidget(self.qlabelList[count], *place)
                    self.btnDate.clicked.connect(self.CalendarWidget.DisplayCalendar)
                    self.CalendarWidget.btnSelect.clicked.connect(self.getDate)

                elif self.AddType == "BookInvoice" and count == 1:
                    self.btnDate = QPushButton("Date", self)
                    self.qlabelList.append(self.btnDate)
                    self.gridLayout.addWidget(self.qlabelList[count], *place)
                    self.btnDate.clicked.connect(self.CalendarWidget.DisplayCalendar)
                    self.CalendarWidget.btnSelect.clicked.connect(self.getDate)

                elif self.AddType == "Royalties" and count == 1:
                    self.btnDate = QPushButton("Date", self)
                    self.qlabelList.append(self.btnDate)
                    self.gridLayout.addWidget(self.qlabelList[count], *place)
                    self.btnDate.clicked.connect(self.CalendarWidget.DisplayCalendar)
                    self.CalendarWidget.btnSelect.clicked.connect(self.getDate)
                
                else:
                    if str(self.columnHeader) == "PubInvoiceService":
                        self.qlabel = QLabel("Service", self)
                    elif str(self.columnHeader) in ["PubInvoicePayment", "BookInvoicePayment", "RoyaltyPayment"]:
                        self.qlabel = QLabel("Payment", self)
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

        elif self.AddType == "PubInvoice":
            self.inputList[3].addItem("Standard")
            self.inputList[3].addItem("Enhanced")
            self.inputList[3].addItem("Colour Publishing")
            self.inputList[3].addItem("Reprint")
        elif self.AddType == "BookInvoiceItems":
            self.inputList[4].addItem("Rush")
            self.inputList[4].addItem("Premium")
            self.inputList[4].addItem("Standard")
            self.inputList[4].addItem("Economy")
            self.inputList[4].addItem("International")
        if self.Editing == True:

            if self.AddType == "Book":

                for count in range(0, 12):
                    try: #for line edits
                        self.inputList[count].setText(self.originalItemList[count])
                    except: #for comboboxes
                        self.originalIndex = self.inputList[count].findText(self.originalItemList[count])
                        self.inputList[count].setCurrentIndex(self.originalIndex)

            elif self.AddType == "PubInvoice":
                
                for count in range(0, 5):
                    try:
                        self.inputList[count].setText(self.originalItemList[count])
                    except:
                        self.originalIndex = self.inputList[count].findText(self.originalItemList[count])
                        self.inputList[count].setCurrentIndex(self.originalIndex)
                        
            elif self.AddType in ["BookInvoice", "Royalties"]:

                for count in range(0, 2):
                    self.inputList[count].setText(self.originalItemList[count])
                    

        self.horizontal = QHBoxLayout()
        if self.AddType == "BookInvoiceItems":
            self.horizontal.addWidget(self.btnCalculate)
            self.horizontal.addWidget(self.qleCalculation)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnCancel)
        self.horizontal.addWidget(self.btnConfirm)

        self.vertical = QVBoxLayout()
        self.vertical.addLayout(self.gridLayout)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)
        if self.Editing == False:
            self.btnConfirm.clicked.connect(self.accept) #accept on clicking confirm

        self.btnCancel.clicked.connect(self.reject) #reject on clicking cancel
        self.exec_()
        
    def AnswerButtons(self):
        self.btnConfirm = QPushButton("Confirm", self)
        self.btnCancel = QPushButton("Cancel", self)
        if self.AddType == "BookInvoiceItems":
            self.btnCalculate = QPushButton("Calculate", self)
            self.qleCalculation = QLineEdit(self)

    def getDate(self):
        self.CalendarWidget.date = self.CalendarWidget.qle.text()
        if self.AddType == "Book":
            self.inputList[10].setText(self.CalendarWidget.date)
            
        elif self.AddType == "PubInvoice":
            self.inputList[2].setText(self.CalendarWidget.date)

        elif self.AddType in ["BookInvoice", "Royalties"]:
            self.inputList[1].setText(self.CalendarWidget.date)
        
    
