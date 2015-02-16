from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys


class initSearchResultsMenu(QWidget):
    """main window"""

    def __init__(self):
        super().__init__()
        self.btnBack = QPushButton("Back", self)
        self.btnBack.setFixedSize(100, 30)
        self.horizontalTop = QHBoxLayout()
        self.horizontalTop.addStretch(1)
        self.horizontalTop.addWidget(self.btnBack)

        self.vertical = QVBoxLayout()
        self.vertical.addLayout(self.horizontalTop)
        self.setLayout(self.vertical)
        
