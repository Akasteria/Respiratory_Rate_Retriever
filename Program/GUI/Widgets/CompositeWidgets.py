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
        self.addTab(w, "Dashboard")
        self.addTab(self.hourlyChart, "Hourly Log")
        self.addTab(self.dailyChart, "Daily Log")
        self.addTab(self.weeklyChart, "Weekly Log")
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
            sCounter = [0,0,0,0]
            for j in range (60):
                min = t - datetime.timedelta(hours=i, minutes=j)
                data = self.database.ReadMinute(min.year, min.month , min.day, min.hour, min.minute)
                d, s = self.DataTranslation(data)
                sCounter[s] = sCounter[s]+1
                if (d == 0):
                    continue
                buffer[0].append(d)
                buffer[1].append(s)
            if (sCounter[0] > 45):
                self.dailyData[0].append(0)
                self.dailyData[1].append(0)
                continue
            self.dailyData[0].append(sum(buffer[0])/len(buffer[0]))
            sCounter[0] = 0
            self.dailyData[1].append(sCounter.index(max(sCounter)))
    def GetWeeklyData(self,t):
        self.weeklyData = [[],[]]
        for i in range(7):
            dayBuffer = [[], []]
            daySCounter = [0,0,0,0]
            for j in range (24):
                buffer = [[], []]
                sCounter = [0,0,0,0]
                for k in range (60):
                    min = t - datetime.timedelta(days=i, hours=j, minutes=k)
                    data = self.database.ReadMinute(min.year, min.month , min.day, min.hour, min.minute)
                    d, s = self.DataTranslation(data)
                    sCounter[s] = sCounter[s]+1
                    if (d == 0):
                        continue
                    buffer[0].append(d)
                    buffer[1].append(s)
                if (sCounter[0] > 45):
                    dayBuffer[0].append(0)
                    dayBuffer[1].append(0)
                    continue
                dayBuffer[0].append(sum(buffer[0])/len(buffer[0]))
                sCounter[0] = 0
                daySCounter[sCounter.index(max(sCounter))] = daySCounter[sCounter.index(max(sCounter))] + 1
            if (daySCounter[0] > 18):
                self.weeklyData[0].append(0)
                self.weeklyData[1].append(0)
                continue 
            self.weeklyData[0].append(sum(dayBuffer[0])/len(dayBuffer[0]))
            daySCounter[0] = 0
            self.weeklyData[1].append(daySCounter.index(max(daySCounter)))
    def DataTranslation(self, data):
        if (len(data) == 0):
            return 0, 0
        if (data[0][-1] == 1):
            return int(data[0][0]), 2
        if (data[0][-2] == 1):
            return int(data[0][0]), 3
        return int(data[0][0]), 1
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
