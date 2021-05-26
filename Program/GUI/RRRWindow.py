from Program.GUI.Widgets.MyWidgets import UserLogin
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ..Tools import Pseudodata
from .Widgets import CompositeWidgets
from ..Database.DataIO import Database
try:
    from ..DataHandlers.SerialReceiver import SerialReceiver as Worker
except:
    from ..Testing.ThreadTester import Worker
    
class RRRWindow():
    def __init__(self, styleSheet):
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(styleSheet)
        self.app.setWindowIcon(QIcon(os.path.dirname(sys.argv[0]) + "\\respirate.png"))
        self.database = Database()
        self.OpenLoginWindow()
        # TODO read from database
    def OpenLoginWindow(self):
        self.login = UserLogin()
        self.login.setWindowIcon(QIcon(os.path.dirname(sys.argv[0]) + "\\respirate.png"))
        self.login.exec_()
        while (self.login.result() == 1):
            name, password, register = self.login.OnAccept()
            if (register):
                self.database.LoadDB(name, password)
                self.database.CreateDatabase()
                self.OpenMainWindow()
                break
            if (self.database.LoadDB(name, password)):
                self.OpenMainWindow()
                break
            else:
                self.login.exec_()
    def OpenMainWindow(self):
        #data = Pseudodata.GenerateSet(60, 15, 0.98, (15,18),False, None, (25,30))
        #data2 = Pseudodata.GenerateSet(24, 6, 0.9, (15,18),True, None, None)
        #data3 = Pseudodata.GenerateSet(7, 1, 0.5, (15,18),False,(20,24))
        self.window = CompositeWidgets.ChartValuePairList(self.database)
        mainw = QMainWindow()
        mainw.setWindowIcon(QIcon(os.path.dirname(sys.argv[0]) + "\\respirate.png"))
        mainw.setCentralWidget(self.window)
        mainw.show()
        mainw.setWindowTitle("Respirate")
        # Setup Serial Read Worker
        self.obj = Worker()
        self.thread = QThread()
        self.obj.minuteReport.connect(self.OnMinuteUpdate)
        self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.thread.quit)
        self.thread.started.connect(self.obj.GetSerial)
        self.thread.start()
        self.app.exec_()
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
