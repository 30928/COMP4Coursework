from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys
import re


class dbAddItemWindow(QDialog):
    """add entry window dialog"""

    def __init__(self):
        super().__init__()
    
    def initAddItemWindow(self):
        self.setWindowTitle("Add {}".format(self.AddType))
        if self.Editing == True:
            self.setWindowTitle("Edit {}".format(self.AddType))
        self.ReadyToVerify = True
        self.setModal(True) #modal window
        self.Calculated = False
        with sqlite3.connect("PP.db") as db: #fetching data from db
            cursor = db.cursor()
            cursor.execute(self.sql)
            db.commit()
            
        self.Columns = []
        self.ColumnNames = cursor.description    
        
        for count in range(0, len(self.ColumnNames)):
            self.Columns.append(list(list(self.ColumnNames)[count])[0])
        self.coordinates = []
        
        for count in range(int(round(len(self.Columns)/2, 1) + 1)):
            for count2 in range(4):
                   self.coordinates.append((count, count2))
                   
        self.ColumnLength = len(self.Columns)              
        for count in range(0, self.ColumnLength):
            self.Columns.insert((count * 2) + 1, "")

        db.close()
        self.inputList = []
        self.qlabelList = []
        self.gridLayout = QGridLayout()
        count = 0

        for self.coordinate, self.columnHeader in zip(self.coordinates, self.Columns):
            
            if self.columnHeader == "": #replacing spaces with line edits

                if self.AddType == "Book" and count in [0, 1, 3, 4, 5, 6, 7, 9, 10, 11]:
                    if count == 0:
                        self.input = QLineEdit(self)
                        self.input.setValidator(QRegExpValidator(QRegExp("[\w]+")))
                    elif count == 1: #exceptions for book
                        self.input = QLineEdit(self) #new line edit
                        self.input.setReadOnly(True)
                        self.input.setText(self.selectedID)
                    elif count in [3, 9, 11]:
                        self.input = QLineEdit(self)
                        if count == 3:
                            self.input.setValidator(QIntValidator())
                        else:
                            self.input.setValidator(QDoubleValidator())
                    elif count in [4, 5, 6, 7]: #exceptions for book where combobox is needed
                        self.input = QComboBox(self) #new combo box

                    elif count == 10:
                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)

                elif self.AddType == "PubInvoice" and count in [0, 1, 2, 3, 4]:
                    
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

                    elif count == 4:
                        self.input = QLineEdit(self)
                        self.input.setValidator(QDoubleValidator())
                
                elif self.AddType in ["BookInvoice", "Royalties"] and count in [0, 1]:

                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)
                        
                        if count == 0:
                            self.input.setText(self.selectedID)
                elif self.AddType == "BookInvoiceItems" and count in [0, 1, 2, 3, 4, 5]:

                    if count == 0:
                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)
                        self.input.setText(self.selectedID)
                    elif count == 1:
                        self.input = QLineEdit(self)
                        self.input.setReadOnly(True)
                        self.input.setText(self.selectedISBN)
                    elif count in [2, 3, 5]:
                        self.input = QLineEdit(self)
                        if count == 2:
                            self.input.setValidator(QIntValidator())
                        else:
                            self.input.setValidator(QDoubleValidator())
                    elif count == 4:
                        self.input = QComboBox(self)
                        
                elif self.AddType == "RoyaltyItems" and count in [0, 1, 3, 4, 5, 6, 7]:
                    with sqlite3.connect("PP.db") as db:
                        cursor = db.cursor()
                        Selection = "NoOfPages, Size, Back"
                        sql = "select {} from Book where ISBN = {}".format(Selection, self.selectedISBN)
                        cursor.execute(sql)
                        self.SelectionList = list(cursor.fetchone())
                        self.NoOfPages = int(self.SelectionList[0])
                        self.Size = self.SelectionList[1]
                        self.Back = self.SelectionList[2]
                        
                        if self.Size == "Large":
                            self.PagePrice = 0.015 * self.NoOfPages
                            if self.Back == "Hard":
                                self.CoverPrice = 5
                            elif self.Back == "Soft":
                                self.CoverPrice = 1
                                
                        elif self.Size == "Small":
                            self.PagePrice = 0.01 * self.NoOfPages
                            if self.Back == "Hard":
                                self.CoverPrice = 4
                            elif self.Back == "Soft":
                                self.CoverPrice = 0.7

                    self.input = QLineEdit(self)

                    if count == 0:
                        self.input.setText(self.selectedID)
                        self.input.setReadOnly(True)
                    elif count == 1:
                        self.input.setText(self.selectedISBN)
                        self.input.setReadOnly(True)
                    elif count in [3, 4, 5, 6, 7]:
                        if count == 5:
                            self.input.setValidator(QIntValidator())
                        elif count == 6:
                            self.input.setReadOnly(True)
                            self.input.setValidator(QDoubleValidator())
                        else:
                            self.input.setValidator(QDoubleValidator())
                else:
                    self.input = QLineEdit(self) #new line edit #standard input method

                self.inputList.append(self.input)   #line edits/combo boxes appended to list for further reference
                self.gridLayout.addWidget(self.inputList[count], *self.coordinate)

                count += 1
                
            else: #adding qlabels with the line edits
                self.DateEntry = False
                if self.AddType == "Book" and count == 10: #adding date button instead of qlabel
                    self.DateEntry = True
                elif self.AddType == "PubInvoice" and count == 2: #data button instead of qlabel
                    self.DateEntry = True
                elif self.AddType == "BookInvoice" and count == 1:
                    self.DateEntry = True
                elif self.AddType == "Royalties" and count == 1:
                    self.DateEntry = True

                else:
                    if str(self.columnHeader) == "PubInvoiceService":
                        self.qlabel = QLabel("Service", self)
                    elif str(self.columnHeader) in ["PubInvoicePayment", "BookInvoicePayment", "RoyaltyPayment"]:
                        self.qlabel = QLabel("Payment", self)
                    elif str(self.columnHeader) in ["BookInvoiceDiscount", "RoyaltyDiscount"]:
                        self.qlabel = QLabel("Discount", self)
                    elif str(self.columnHeader) in ["BookInvoiceQuantity", "RoyaltyQuantity"]:
                        self.qlabel = QLabel("Quantity", self)
                    elif str(self.columnHeader) == "ExcRateFromGBP":
                        self.qlabel = QLabel("£1 = ", self)
                    elif str(self.columnHeader)[-2:] in ["ID", "BN"]:
                        self.qlabel = QLabel(str(self.columnHeader))
                    
                    else:
                        self.Label = str(self.columnHeader)
                        self.LabelLength = len(self.Label)
                        self.CamelCase = False
                        for count2 in range(1, self.LabelLength):
                            if self.CamelCase == True:
                                pass
                            else:
                                self.CamelCase = False
                            if self.Label[count2].isupper() == True:
                                self.String1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', self.Label[0:count2])
                                self.String2 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', self.Label[count2:self.LabelLength])
                                self.tempLabel = "{} {}".format(self.String1, self.String2)
                                self.CamelCase = True
                        
                        if self.CamelCase == True:
                            self.Label = self.tempLabel

                        self.qlabel = QLabel(str(self.Label), self)
                    self.qlabelList.append(self.qlabel)
                    self.gridLayout.addWidget(self.qlabelList[count], *self.coordinate)
                    
                if self.DateEntry == True:
                    self.btnDate = QPushButton("Date", self)
                    self.qlabelList.append(self.btnDate)
                    self.gridLayout.addWidget(self.qlabelList[count], *self.coordinate)
                    self.btnDate.clicked.connect(self.CalendarWidget.DisplayCalendar)
                    self.CalendarWidget.btnSelect.clicked.connect(self.getDate)
                    
        if self.AddType == "Book":
            self.inputList[4].addItem("Large")
            self.inputList[4].addItem("Small")
            self.inputList[5].addItem("Hard")
            self.inputList[5].addItem("Soft")
            self.inputList[6].addItem("Matte")
            self.inputList[6].addItem("Gloss")
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
                        self.inputList[count].setText(str(self.originalItemList[count]))
                    except: #for comboboxes
                        self.originalIndex = self.inputList[count].findText(str(self.originalItemList[count]))
                        self.inputList[count].setCurrentIndex(self.originalIndex)

            elif self.AddType == "PubInvoice":
                
                for count in range(0, 5):
                    try:
                        self.inputList[count].setText(str(self.originalItemList[count]))
                    except:
                        self.originalIndex = self.inputList[count].findText(str(self.originalItemList[count]))
                        self.inputList[count].setCurrentIndex(self.originalIndex)
                        
            elif self.AddType in ["BookInvoice", "Royalties"]:

                for count in range(0, 2):
                    self.inputList[count].setText(str(self.originalItemList[count]))
            elif self.AddType == "BookInvoiceItems":
                for count in range(0, 6):
                    try:
                        self.inputList[count].setText(str(self.originalItemList[count]))
                    except:
                        self.originalIndex = self.inputList[count].findText(str(self.originalItemList[count]))
                        self.inputList[count].setCurrentIndex(self.originalIndex)
            elif self.AddType == "RoyaltyItems":
                for count in range(0, 8):
                    self.inputList[count].setText(str(self.originalItemList[count]))

        self.horizontal = QHBoxLayout()
        if self.AddType in ["BookInvoiceItems", "RoyaltyItems"]:
            self.horizontal.addWidget(self.btnCalculate)
            self.horizontal.addWidget(self.qleCalculation)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(self.btnCancel)
        self.horizontal.addWidget(self.btnConfirm)
        if self.AddType in ["BookInvoiceItems", "RoyaltyItems"]:
            if self.Editing == False:
                self.btnConfirm.clicked.connect(self.CheckCalculated)
        if self.Editing == False:
            self.btnConfirm.clicked.connect(self.Validate)
        self.vertical = QVBoxLayout()
        self.vertical.addLayout(self.gridLayout)
        self.vertical.addLayout(self.horizontal)
        self.setLayout(self.vertical)

                
        self.btnCancel.clicked.connect(self.reject) #reject on clicking cancel
        self.exec_()

    def CheckCalculated(self):
        self.ReadyToVerify = False
        if len(self.qleCalculation.text()) == 0:
            self.Msg = QMessageBox()
            self.Msg.setWindowTitle("Calculation")
            self.Msg.setText("You must fill all fields and click 'Calculate' before attempting to add to the database.")
            self.Msg.exec_()
        else:
            self.ReadyToVerify = True

    def AnswerButtons(self): #so connections can be made outside of this class
        self.btnConfirm = QPushButton("Confirm", self)
        self.btnCancel = QPushButton("Cancel", self)
        if self.AddType in ["BookInvoiceItems", "RoyaltyItems"]:
            self.btnCalculate = QPushButton("Calculate", self)
            self.qleCalculation = QLineEdit(self)
            self.qleCalculation.setReadOnly(True)

    def getDate(self):
        self.CalendarWidget.date = self.CalendarWidget.qle.text()
        if self.AddType == "Book":
            self.inputList[10].setText(self.CalendarWidget.date)
            
        elif self.AddType == "PubInvoice":
            self.inputList[2].setText(self.CalendarWidget.date)

        elif self.AddType in ["BookInvoice", "Royalties"]:
            self.inputList[1].setText(self.CalendarWidget.date)

    def keyReleaseEvent(self, QKeyEvent):
        if self.AddType == "RoyaltyItems":
            if self.inputList[2].text() == "£":
                self.inputList[7].setText("N/A")
                self.inputList[7].setReadOnly(True)
            elif self.inputList[7].text() == "N/A": 
                self.inputList[7].setText("")
                self.inputList[7].setReadOnly(False)
            if self.inputList[5].text() != "":
                self.PrintCost = (self.PagePrice + self.CoverPrice) * int(self.inputList[5].text())
                self.inputList[6].setText("{0:.2f}".format(self.PrintCost))
            elif self.inputList[5].text() == "":
                self.inputList[6].clear()



    def Validate(self):
        if self.ReadyToVerify == True:
            self.input_data = []
            self.Valid = True
            for count in range(0, len(self.inputList)):
                try: #gathering the input data
                    self.input_data.append(str(self.inputList[count].currentText()))
                except:
                    if count == 8 and self.AddType == "RoyaltyItems":
                        self.input_data.append(self.NetSales)
                    else:
                        self.input_data.append(self.inputList[count].text())
                        
            for count in range(0, len(self.input_data)):
                
                if str(self.input_data[count]).replace(" ", "") == "": #presence check
                    self.Valid = False
                    self.ErrorMessage = "All Fields must be filled."
                    break
                try:
                    if float(self.input_data[count]) < 0: #range check
                        self.Valid = False
                        self.ErrorMessage = "Invalid Entry - Please check the fields."
                        break
                except:
                    pass
                
                if self.qlabelList[count].text() == "ISBN":
                    if len(self.input_data[count]) != 13 and len(self.input_data[count]) != 10: #isbn must be 10 or 13 digits
                        self.Valid = False
                        self.ErrorMessage = "Invalid ISBN - Must be 10 or 13 digits."
                        break
                elif self.qlabelList[count].text() == "No Of Pages":
                    if int(self.input_data[count]) > 2000:
                        self.Valid = False
                        self.ErrorMessage = "Invalid Entry - Please check the fields."
                        break
                elif self.qlabelList[count].text() == "Discount": #%'s must be between 0 and 100
                    if float(self.input_data[count]) > 100 or float(self.input_data[count]) < 0:
                        self.Valid = False
                        self.ErrorMessage = "Invalid Entry - Please check the fields."
                        break
                    
            if self.Valid == False:
                self.Msg = QMessageBox()
                self.Msg.setWindowTitle("Invalid Entry")
                self.Msg.setText(self.ErrorMessage)
                self.Msg.exec_()
            else:
                if self.AddType not in ["BookInvoiceItems", "RoyaltyItems"]:
                    if self.Editing == False:
                        self.accept()
                    else:
                        self.ReadyToVerify = True
