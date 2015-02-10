from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class dbInvalidEntry(QDialog):
    """invalid entry dialog"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invalid Entry")
        self.setFixedSize(275, 150)
        self.setModal(True)
        self.Msg = "The following entries were invalid: {}".format(self.Entries)
        self.lblMsg = QLabel(self.Msg, self)
        self.lblMsg.move(50,50)
        self.lblMsg.setWordWrap(True)
        self.lblMsg.setFixedSize(250,50)
        self.lblMsg.setAlignment(Qt.AlignHCenter)
