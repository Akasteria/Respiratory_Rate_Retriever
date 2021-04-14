# main.py
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
import sys
import time
import random

class Worker(QObject):
    finished = pyqtSignal()
    minuteReport = pyqtSignal(float)
    @pyqtSlot()
    def GetSerial(self): # A slot takes no params
        for i in range(1, 100):
            time.sleep(1)
            self.minuteReport.emit(random.randint(15,20))
        self.finished.emit()