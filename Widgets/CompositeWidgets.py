from .MyWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class ChartValuePair(QGroupBox):
    def __init__(self, data, title, xLabel, text):
        QGroupBox.__init__(self)
        chart = BarChart()
        chart.Plot(data, title, xLabel, 'Respiratory Rate')
        #value = ValuePanel(text, data[0][-1], data[1][-1])
        layout = QHBoxLayout()
        layout.addWidget(chart)
        self.setLayout(layout)
class ChartValuePairList(QWidget):
    def __init__(self, hourlyData, dailyData, weeklyData):
        QWidget.__init__(self)
        hourlyChart = ChartValuePair(hourlyData, 'Hourly Trend', 'Time (mins)', 'Current:')
        dailyChart = ChartValuePair(dailyData, 'Daily Trend', 'Time (hours)', 'Hourly Average:')
        weeklyChart = ChartValuePair(weeklyData, 'Weekly Trend', 'Time (Days)', 'Daily Average:')
        vb = QVBoxLayout()
        vb.addWidget(hourlyChart)
        vb.addWidget(dailyChart)
        vb.addWidget(weeklyChart)
        self.setLayout(vb)

class GridWindow(QWidget):
    pass
