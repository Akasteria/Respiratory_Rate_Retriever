from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib import pyplot
from matplotlib.transforms import *
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
class LineChart(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        pyplot.style.use(['dark_background'])
        #matplotlib.use('Qt5Agg')
        self.fig = Figure()
        FigureCanvasQTAgg.__init__(self,self.fig)
        #self.figureCanvas.updateGeometry()
        #self.figureCanvas.draw()
    def Plot(self, data, title, xLabel, yLabel):
        xMin = 1-len(data[0])
        yMax = int(max(data[0]))+1
        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.set_title(title)
        ax.plot(range((xMin), 1), data[0])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_color('gray')
        ax.spines['left'].set_bounds((0, yMax))
        ax.spines['bottom'].set_bounds((xMin, 0))
        ax.set_xlim(left = xMin, right=0)
        ax.set_ylim(bottom = 0, top = yMax)
        ax.grid(True, 'major', clip_on = True, ls='solid', lw=0.5, color='gray')
        self.draw()
        # TODO plot color blocks
    



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