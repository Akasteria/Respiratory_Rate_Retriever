from .MyWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class BarChartLayout(QGroupBox):
    def __init__(self, data, title, xLabel):
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
        self.setTabBar(TabBar(self))
        dashBoard = BarThumbnail()
        dashBoard.Plot(hourlyData, dailyData, weeklyData)
        web = InfoPage()
        w = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(web)
        layout.addWidget(dashBoard)
        w.setLayout(layout)
        hourlyChart = BarChartLayout(hourlyData, 'Hourly Trend', 'Time (mins)')
        dailyChart = BarChartLayout(dailyData, 'Daily Trend', 'Time (hours)')
        weeklyChart = BarChartLayout(weeklyData, 'Weekly Trend', 'Time (Days)')
        self.addTab(w, "Dashboard")
        self.addTab(hourlyChart, "Hourly Log")
        self.addTab(dailyChart, "Daily Log")
        self.addTab(weeklyChart, "Weekly Log")
        self.setTabPosition(QTabWidget.West)
        self.setWindowTitle("RRR")

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
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt);
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
