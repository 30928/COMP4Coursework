from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3
import sys

class OpenDBScreen(QDialog):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Choose database")
        self.setFixedSize(617,90)
        self.setModal(True) #modal window
