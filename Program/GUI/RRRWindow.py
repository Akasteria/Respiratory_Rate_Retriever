import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ..Tools import Pseudodata
from .Widgets import CompositeWidgets
from ..DataHandlers.SerialReceiver import SerialReceiver as Worker
    
class RRRWindow():
    def __init__(self, styleSheet):
        app = QApplication(sys.argv)
        app.setStyleSheet(styleSheet)
        # TODO read from database
        data = Pseudodata.GenerateSet(60, 15, 0.98, (15,18),False, None, (25,30))
        data2 = Pseudodata.GenerateSet(24, 6, 0.9, (15,18),True, None, None)
        data3 = Pseudodata.GenerateSet(7, 1, 0.5, (15,18),False,(20,24))
        self.window = CompositeWidgets.ChartValuePairList(data,data2,data3)
        mainw = QMainWindow()
        mainw.setCentralWidget(self.window)
        mainw.show()
        mainw.setWindowTitle("Respiratory Rate Retriever")
        # Setup Serial Read Worker
        self.obj = Worker()
        self.thread = QThread()
        self.obj.minuteReport.connect(self.OnMinuteUpdate)
        self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.thread.quit)
        self.thread.started.connect(self.obj.GetSerial) # TODO change to serial read
        self.thread.start()
        app.exec_()
    def OnMinuteUpdate(self, minuteReading):
        pastData = self.window.hourlyChart.chart.data
        pastData[0].append(float(minuteReading))
        pastData[0].pop(0)
        # TODO outlier detection
        pastData[1].append(int(1)) # assume everything is normal for now
        pastData[1].pop(0)
        self.window.hourlyChart.chart.UpdatePlot(pastData)
    def Show(self):
        self.app.exec_()
