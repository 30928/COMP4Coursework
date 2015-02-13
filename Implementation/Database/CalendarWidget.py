import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class dbCalendarWidget(QDialog):
    
    def __init__(self):
        super().__init__()
    
    def Calendar(self):
        self.setFixedSize(265, 275)
        self.setWindowTitle('Calendar')
        calendar = QCalendarWidget(self)
        calendar.setGridVisible(True)
        calendar.clicked[QDate].connect(self.date)
        date = calendar.selectedDate()
        self.lblInstruction = QLabel(self)
        self.lblInstruction.setText("Please select a date")
        self.lblInstruction.setAlignment(Qt.AlignCenter)
        self.qle = QLineEdit(self)
        self.qle.setText(date.toString("dd-MM-yyyy"))
        self.qle.setFixedSize(85,20)
        self.qle.setAlignment(Qt.AlignCenter)
        self.btnSelect = QPushButton("Select", self)
        self.btnCancel = QPushButton("Cancel", self)

        self.horizontalTop = QHBoxLayout()
        self.horizontalTop.addStretch(1)
        self.horizontalTop.addWidget(self.lblInstruction)
        self.horizontalTop.addStretch(1)
        
        self.horizontalMid1 = QHBoxLayout()
        self.horizontalMid1.addStretch(1)
        self.horizontalMid1.addWidget(calendar)
        self.horizontalMid1.addStretch(1)

        self.horizontalMid2 = QHBoxLayout()
        self.horizontalMid2.addStretch(1)
        self.horizontalMid2.addWidget(self.qle)
        self.horizontalMid2.addStretch(1)

        self.horizontalBottom = QHBoxLayout()
        self.horizontalBottom.addWidget(self.btnCancel)
        self.horizontalBottom.addStretch(1)
        self.horizontalBottom.addWidget(self.btnSelect)
        
        self.vertical = QVBoxLayout()
        self.vertical.addLayout(self.horizontalTop)
        self.vertical.addLayout(self.horizontalMid1)
        self.vertical.addLayout(self.horizontalMid2)
        self.vertical.addLayout(self.horizontalBottom)
        self.setLayout(self.vertical)

        
    def DisplayCalendar(self):
        self.setModal(True)
        self.btnSelect.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.exec_()
        
    def date(self, date):
        self.qle.setText(date.toString("dd-MM-yyyy"))


