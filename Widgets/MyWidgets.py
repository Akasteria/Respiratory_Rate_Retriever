from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib import pyplot
from matplotlib.patches import Patch
import numpy
import matplotlib
from matplotlib import transforms
from .ColorPalette import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class BarChart(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        pyplot.style.use(['dark_background'])
        matplotlib.use('Qt5Agg')
        self.fig = Figure()
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.currentPatch = None
        self.fig.canvas.mpl_connect('motion_notify_event', self.OnMouseMove)
        self.fig.canvas.mpl_connect('axes_leave_event', self.OnLeaveAxis)

    def Plot(self, data, title, xLabel, yLabel):
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.title = title
        self.data = data
        self.UpdatePlot(data)

    def UpdatePlot(self, data):
        xMin = -len(data[0])
        yMax = int(max(data[0]) * 1.3)  # leave space for legend
        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.set_xlabel(self.xLabel)
        ax.set_ylabel(self.yLabel)
        ax.set_title(self.title)
        # Plot bar chart
        #ax.plot(range(xMin, 1), data[0])
        bars = ax.bar(range(xMin, 0), data[0],
                      width=1, align='edge', linewidth=2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_color('gray')
        ax.spines['left'].set_bounds((0, yMax))
        ax.spines['bottom'].set_bounds((xMin, 0))
        ax.set_xlim(left=xMin, right=0)
        ax.set_ylim(bottom=0, top=yMax)

        # Color bars
        myInt = 0
        self.patches = bars.patches
        for patch in self.patches:
            patch.set_facecolor(UIColors(data[1][myInt]))
            myInt = myInt + 1
        # Setup legend
        legendElements = []
        for i in range(len(UIColor)):
            if (i in data[1]):
                legendElements.append(Patch(facecolor=UIColors(i), linewidth=1, edgecolor=(
                    None), label=ColorToDescription(UIColors(i))))
        ax.legend(handles=legendElements, loc='upper right')
        # Draw annotation
        self.annot = ax.annotate(text="", xy=(0, 0), xytext=(10, 10), xycoords="data", textcoords='offset pixels',
                                 annotation_clip=False, bbox=dict(boxstyle='square', ec=(0.8, 0.8, 0.8), fc=UIColor.EMPTY.value, lw=1), visible=False)
        # Draw grid and update
        ax.get_yaxis().grid(True, 'major', clip_on=True, ls='solid', lw=0.5, color='gray')
        self.draw()

    def OnMouseMove(self, event):
        if (event.xdata != None and event.ydata > 0 and event.ydata <= self.data[0][len(self.patches) + int(event.xdata) - 1]):
            newPatch = self.patches[len(
                self.patches) + int(event.xdata+0.01) - 1]
            # annotation
            self.annot.xy = (event.xdata, event.ydata)
            if (newPatch != self.currentPatch):
                if (self.currentPatch != None):
                    self.currentPatch.set_edgecolor(None)
                    self.currentPatch.set_zorder(1)
                if (newPatch != None):
                    self.annot.set_visible(True)
                    self.annot.set_text('Time: {:d}\nRespiratory Rate: {:.1f}'.format(int(
                        event.xdata+0.01), self.data[0][len(self.patches) + int(event.xdata+0.01) - 1]))
                    newPatch.set_edgecolor((1, 1, 1))
                    newPatch.set_zorder(2)
                    # print(newPatch.zorder)
                self.currentPatch = newPatch
        else:
            self.annot.set_visible(False)
            if (self.currentPatch != None):
                self.currentPatch.set_edgecolor(None)
                self.currentPatch.set_zorder(1)
                self.currentPatch = None
        self.draw()

    def OnLeaveAxis(self, event):
        self.annot.set_visible(False)
        if (self.currentPatch != None):
            self.currentPatch.set_edgecolor(None)
            self.currentPatch.set_zorder(1)
            self.currentPatch = None
            self.draw()


class PieChart(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        pyplot.style.use(['dark_background'])
        matplotlib.use('Qt5Agg')
        self.fig = Figure()
        FigureCanvasQTAgg.__init__(self, self.fig)

    @staticmethod
    def ConvertToFrequency(data):
        i = 0
        npData = numpy.array(data[1])
        pieData = []
        while (i <= max(data[1])):
            pieData.append(numpy.count_nonzero(npData == i))
            i = i + 1
        return pieData

    @staticmethod
    def AddPercentages(strings, pieData):
        total = sum(pieData)
        labels = []
        for i in range(len(pieData)):
            if pieData[i] > 0:
                labels.append('{:d} ({:.1f}%)\n{}'.format(
                    pieData[i], pieData[i]/total*100, strings[i]))
                continue
            labels.append('')
        return labels

    def Plot(self, data):
        pieData = self.ConvertToFrequency(data)
        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.pie(pieData, labels=self.AddPercentages(
            Descriptions(), pieData), colors=UIColors())

        legendElements = []
        for i in range(len(UIColor)):
            if (i in data[1]):
                legendElements.append(Patch(facecolor=UIColors(
                    i), linewidth=0, label=ColorToDescription(UIColors(i))))
        self.draw()


class ValuePanel(QWidget):
    def __init__(self, text, value, status):
        QWidget.__init__(self)
        uiText = QLabel()
        uiText.setText(StyledText(text, (1, 1, 1), 24, 'Times'))
        self.uiValue = QLabel()
        self.uiValue.setText(StyledText(
            '<b>'+str(int(value))+'</b>', BrightUIColors(status), 40, 'Times'))

        layout = QVBoxLayout()
        layout.addWidget(uiText)
        layout.addWidget(self.uiValue)
        self.setLayout(layout)

    def ChangeValue(self, value, status):
        self.uiValue = QLabel()
        self.uiValue.setText(StyledText(
            '<b>'+str(int(value))+'</b>', BrightUIColors(status), 40, 'Times'))
