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
class ChartValuePairList(QTabWidget):
    def __init__(self, hourlyData, dailyData, weeklyData):
        QTabWidget.__init__(self)
        dashBoard = BarThumbnail()
        dashBoard.Plot(hourlyData, dailyData, weeklyData)
        hourlyChart = ChartValuePair(hourlyData, 'Hourly Trend', 'Time (mins)', 'Current:')
        dailyChart = ChartValuePair(dailyData, 'Daily Trend', 'Time (hours)', 'Hourly Average:')
        weeklyChart = ChartValuePair(weeklyData, 'Weekly Trend', 'Time (Days)', 'Daily Average:')
        self.addTab(dashBoard, "Dash Board")
        self.addTab(hourlyChart, "Hourly Log")
        self.addTab(dailyChart, "Daily Log")
        self.addTab(weeklyChart, "Weekly Log")
        self.setTabPosition(QTabWidget.West)
        self.setWindowTitle("RRR")
