import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ..Tools import Pseudodata
from .Widgets import CompositeWidgets
class RRRWindow():
    def __init__(self, styleSheet):
        app = QApplication(sys.argv)
        app.setStyleSheet(styleSheet)
        data = Pseudodata.GenerateSet(60, 15, 0.98, (15,18),False, None, (25,30))
        data2 = Pseudodata.GenerateSet(24, 6, 0.9, (15,18),True, None, None)
        data3 = Pseudodata.GenerateSet(7, 1, 0.5, (15,18),False,(20,24))
        self.window = CompositeWidgets.ChartValuePairList(data,data2,data3)
        mainw = QMainWindow()
        mainw.setCentralWidget(self.window)
        mainw.show()
        mainw.setWindowTitle("Respiratory Rate Retriever")
        app.exec_()
    def SetData(self, minuteReading):
        pastData = self.window.hourlyChart.data
        pastData.append(minuteReading)
        pastData.pop(0)
        self.window.hourlyChart.Plot(pastData)
        pass