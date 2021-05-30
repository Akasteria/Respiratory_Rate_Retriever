from .MyWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
import time
class BarChartLayout(QGroupBox):
    def __init__(self, data, title, xLabel):
        QGroupBox.__init__(self)
        self.chart = BarChart()
        self.chart.Plot(data, title, xLabel, 'Respiratory Rate')
        layout = QHBoxLayout()
        layout.addWidget(self.chart)
        self.setLayout(layout)
class ChartValuePairList(QTabWidget):
    def __init__(self, database):
        QTabWidget.__init__(self)
        self.database = database
        self.setTabBar(TabBar(self))
        dashBoard = BarThumbnail(self.TabToHourly, self.TabToDaily, self.TabToWeekly)
        self.UpdateAll()
        dashBoard.Plot(self.hourlyData, self.dailyData, self.weeklyData)
        web = InfoPage()
        w = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(web)
        layout.addWidget(dashBoard)
        w.setLayout(layout)
        self.hourlyChart = BarChartLayout(self.hourlyData, 'Hourly Trend', 'Time (mins)')
        self.dailyChart = BarChartLayout(self.dailyData, 'Daily Trend', 'Time (hours)')
        self.weeklyChart = BarChartLayout(self.weeklyData, 'Weekly Trend', 'Time (Days)')
        self.history = QWidget()
        h = QHBoxLayout()
        b1 = QGroupBox()
        b1.setTitle("Starting date")
        b1.setStyleSheet("color: white;")
        t = QHBoxLayout()
        c = QCalendarWidget()
        c.setStyleSheet("alternate-background-color: #555555;")
        t.addWidget(c)
        b1.setLayout(t)
        b2 = QGroupBox()
        b2.setTitle("Ending date")
        b2.setStyleSheet("color: white;")
        t = QHBoxLayout()
        c = QCalendarWidget()
        c.setStyleSheet("alternate-background-color: #6D6D6D;")
        t.addWidget(c)
        b2.setLayout(t)
        h.addWidget(b1)
        h.addWidget(b2)
        self.history.setLayout(h)
        self.addTab(w, "Dashboard")
        self.addTab(self.hourlyChart, "Hourly Log")
        self.addTab(self.dailyChart, "Daily Log")
        self.addTab(self.weeklyChart, "Weekly Log")
        self.addTab(self.history, "View History")
        self.setTabPosition(QTabWidget.West)
        self.setWindowTitle("RRR")
    def TabToHourly(self):
        self.setCurrentIndex(1)
    def TabToDaily(self):
        self.setCurrentIndex(2)
    def TabToWeekly(self):
        self.setCurrentIndex(3)
    def UpdateAll(self):
        t = datetime.datetime(time.gmtime()[0],time.gmtime()[1],time.gmtime()[2],time.gmtime()[3],time.gmtime()[4],time.gmtime()[5],time.gmtime()[6],None)
        self.GetHourlyData(t)
        self.GetDailyData(t)
        self.GetWeeklyData(t)
    def UpdateAllPlot(self):
        self.hourlyChart.chart.UpdatePlot(self.hourlyData)
        self.dailyChart.chart.UpdatePlot(self.dailyData)
        self.weeklyChart.chart.UpdatePlot(self.weeklyData)
    def GetHourlyData(self, t):
        self.hourlyData = [[],[]]
        for i in range(60):
            min = t - datetime.timedelta(minutes=i)
            data = self.database.ReadMinute(min.year, min.month , min.day, min.hour, min.minute)
            d, s = self.DataTranslation(data)
            self.hourlyData[0].append(d)
            self.hourlyData[1].append(s)
    def GetDailyData(self, t):
        self.dailyData = [[],[]]
        for i in range (24):
            buffer = [[], []]
            for j in range (60):
                min = t - datetime.timedelta(hours=i, minutes=j)
                data = self.database.ReadMinute(min.year, min.month , min.day, min.hour, min.minute)
                d, s = self.DataTranslation(data)
                buffer[0].append(d)
                buffer[1].append(s)
            avg = self.CalculateAverage(buffer, False)
            self.dailyData[0].append(avg[0])
            self.dailyData[1].append(avg[1])
    def GetWeeklyData(self,t):
        self.weeklyData = [[],[]]
        for i in range(7):
            dayBuffer = [[], []]
            for j in range (24):
                buffer = [[], []]
                for k in range (60):
                    min = t - datetime.timedelta(days=i, hours=j, minutes=k)
                    data = self.database.ReadMinute(min.year, min.month , min.day, min.hour, min.minute)
                    d, s = self.DataTranslation(data)
                    buffer[0].append(d)
                    buffer[1].append(s)
                avg = self.CalculateAverage(buffer, True)
                dayBuffer[0].append(avg[0])
                dayBuffer[1].append(avg[1])
            dayAvg = self.CalculateAverage(dayBuffer, True)
            self.weeklyData[0].append(dayAvg[0])
            self.weeklyData[1].append(dayAvg[1])
    def DataTranslation(self, data):
        if (len(data) == 0):
            return 0, 0
        if (int(data[0][-2]) == 1):
            return int(data[0][0]), 2
        if (int(data[0][-1]) == 1):
            return int(data[0][0]), 3
        return int(data[0][0]), 1
    def CalculateAverage(self, data, excludeExercise):
        count = [[],[0,0,0,0]]
        for i in range(len(data[0])): 
            if excludeExercise and (data[1][i] == 0 or data[1][i] == 3):
                continue
            count[0].append(data[0][i])
            count[1][data[1][i]] = count[1][data[1][i]] + 1
        if (len(count[0]) == 0):
            return [0,0]
        avg = sum(count[0])/len(count[0])
        stat = 1
        if (count[1][2]>0):
            stat = 2
        if (count[1][3]>0):
            stat = 3
        return [avg, stat]
class TabBar(QTabBar):
    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()

class ProxyStyle(QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QStyle.PM_TabBarIconSize)
            r = QRect(opt.rect)
            w =  0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QProxyStyle.drawControl(self, element, opt, painter, widget)
