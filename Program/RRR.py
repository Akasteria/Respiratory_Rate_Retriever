import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .GUI import RRRWindow
def ShowGUI(styleSheet):
    window = RRRWindow.RRRWindow(styleSheet)