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
        self.axB, self.axP = self.fig.subplots(ncols=2, nrows=1)
        self.fig.canvas.mpl_connect('motion_notify_event', self.OnMouseMove)
        self.fig.canvas.mpl_connect('axes_leave_event', self.OnLeaveAxis)

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

    def Plot(self, data, title, xLabel, yLabel):
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.title = title
        self.data = data
        self.UpdatePlot(data)

    def UpdatePlot(self, data):
        self.UpdateBar(data)
        self.UpdatePie(data)
        self.DrawAnnotation()
        self.draw()
    def UpdateBar(self,data):
        xMin = -len(data[0])
        yMax = int(max(data[0]) * 1.3)  # leave space for legend
        self.axB.clear()
        self.axB.set_xlabel(self.xLabel)
        self.axB.set_ylabel(self.yLabel)
        self.axB.set_title(self.title)
        # Plot bar chart
        #axB.plot(range(xMin, 1), data[0])
        bars = self.axB.bar(range(xMin, 0), data[0],
                      width=1, align='edge', linewidth=2)
        self.axB.spines['top'].set_visible(False)
        self.axB.spines['right'].set_color('gray')
        self.axB.spines['left'].set_bounds((0, yMax))
        self.axB.spines['bottom'].set_bounds((xMin, 0))
        self.axB.set_xlim(left=xMin, right=0)
        self.axB.set_ylim(bottom=0, top=yMax)

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
        self.axB.legend(handles=legendElements, loc='upper right')
        # Draw grid
        self.axB.get_yaxis().grid(True, 'major', clip_on=True, ls='solid', lw=0.5, color='gray')
    def UpdatePie(self, data):
        pieData = self.ConvertToFrequency(data)
        self.axP.clear()
        self.axP.pie(pieData, labels=self.AddPercentages(
            Descriptions(), pieData), colors=UIColors())

        legendElements = []
        for i in range(len(UIColor)):
            if (i in data[1]):
                legendElements.append(Patch(facecolor=UIColors(
                    i), linewidth=0, label=ColorToDescription(UIColors(i))))
    def DrawAnnotation(self):
        # Draw annotation
        self.annot = self.axB.annotate(text="", xy=(0, 0), xytext=(10, 10), xycoords="data", textcoords='offset pixels',
                                 annotation_clip=False, bbox=dict(boxstyle='square', ec=(0.8, 0.8, 0.8), fc=UIColor.EMPTY.value, lw=1), visible=False)
    def Focus(self, artist):
        artist.set_edgecolor((1, 1, 1))
        artist.set_zorder(2)
    def Defocus(self, artist):
        if (artist != None):
            self.annot.set_visible(False)
            artist.set_edgecolor(None)
            artist.set_zorder(1)
            artist = None
    def OnMouseMove(self, event):
        if (event.xdata != None and event.ydata > 0 and event.ydata <= self.data[0][len(self.patches) + int(event.xdata) - 1]):
            newPatch = self.patches[len(
                self.patches) + int(event.xdata+0.01) - 1]
            # annotation
            self.annot.xy = (event.xdata, event.ydata)
            if (newPatch != self.currentPatch):
                self.Defocus(self.currentPatch)
                self.annot.set_visible(True)
                self.annot.set_text('Time: {:d}\nRespiratory Rate: {:.1f}'.format(int(
                    event.xdata+0.01), self.data[0][len(self.patches) + int(event.xdata+0.01) - 1]))
                self.Focus(newPatch)
                # print(newPatch.zorder)
                self.currentPatch = newPatch
        else:
            self.Defocus(self.currentPatch)
        self.draw()

    def OnLeaveAxis(self, event):
        self.Defocus(self.currentPatch)


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
