from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib import pyplot
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
class QLineChart(QWidget):
    def __init__(self, left, top, width, height):
        super().__init__()
        matplotlib.use('Qt5Agg')
        rect = QRect(left, top, width, height) #TODO flexible dimentions, minimum size hint
        self.setGeometry(rect)
        self.setMinimumSize(width + 2 * left, height + 2 * top)
        self.CreateCanvas()
    def UpdateChart(self, ax, fig):
        self.ax = ax
        self.fig = fig
        self.draw
    def CreateCanvas(self):
        pyplot.style.use(['dark_background'])
        self.fig, self.ax = pyplot.subplots()
        self.figureCanvas = FigureCanvasQTAgg(self.fig)        
        self.figureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        self.figureCanvas.updateGeometry(self)
        self.figureCanvas.move(0,0)
        self.figureCanvas.draw()
    def SetLabels(self, xLabel, yLabel):
        self.ax.set_xlabel(xLabel)
        self.ax.set_ylabel(yLabel)
    def Plot(self, data):
        self.ax.plot(range(1-len(data[0]), 1), data[0])
        # TODO plot color blocks
    



class LineChart():
    def __init__(self, data, span, xLabel, yLabel, title, left, top, width, height):
        # data is a list of tuple (x,y,b)
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.title = title
        self.chartData = []
        self.totalTime = data[-1][0] - data[0][0]
        self.span = span
        for unitData in data:
            #print(unitData)
            self.Add(unitData)
        # Setup plot backend, plot style
        self.widget = QLineChart(left, top, width, height, self)
        
    def Add(self, unitData):
        self.Enqueue(unitData)
        while (self.totalTime > self.span):
            self.Dequeue()
    def Enqueue(self, unitData):
        self.totalTime = self.totalTime + unitData[0]
        self.chartData.append(unitData)
    def Dequeue(self):
        self.totalTime = self.totalTime - self.chartData[0][0]
        self.chartData.pop(0)

    def DrawGrid(self):
        self.scene.addline()
    def PlotData(self, ax):
        x = []
        y = []
        xSum = 0
        for unitdata in self.chartData:
            x.append(xSum)
            y.append(unitdata[1])
            xSum = xSum+unitdata[0]
        ax.plot(x,y)
        ax.set_xlabel(self.xLabel)  # Add an x-label to the axes.
        ax.set_ylabel(self.yLabel)  # Add a y-label to the axes.
        ax.set_title(self.title)  # Add a title to the axes.
        ax.grid() # Show grid
