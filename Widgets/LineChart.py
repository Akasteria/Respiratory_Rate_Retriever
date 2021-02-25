from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class LineChart():
    def __init__(self, data, span, xLabel, yLabel, title, minXSize, minYSize):
        # data is a list of tuple (x,y,b)
        self.chartData = []
        self.totalTime = data[-1][0] - data[0][0]
        self.span = span
        for unitData in data:
            self.Add(unitData)
        
    def Add(self, unitData):
        self.Enqueue(unitData)
        while (self.totalTime > self.span):
            self.Dequeue()
    def Enqueue(self, unitData):
        self.totalTime = self.totalTime + unitData[0][0]
        self.chartData.append(unitData)
    def Dequeue(self):
        self.totalTime = self.totalTime - self.chartData[0][0]
        self.chartData.pop(0)
    def CreateWidget(self, xLabel, yLabel, title, minXSize, minYSize):
        self.widget = QGraphicsView()
        self.scene = QGraphicsScene()
        self.widget.setScene(self.scene)
    def DefinePens(self):
        # Axis line
        self.axisPen = QPen(QColorConstants.White)
        self.axisPen.setWidth(2)
        # Grid line
        self.gridPen = QPen(QColorConstants.White)
        self.gridPen.setWidth(1)
        # Plot line
        self.plotLine = QPen(QColor(100,100,255,180))
        self.plotLine.setWidth(2)
        # Transparent line
        self.transparentLine = QPen(QColor(0,0,0,0))
    def DrawGrid(self):
        self.scene.addline()
    def PlotData(self, absoluteTime, magnitude):
        
