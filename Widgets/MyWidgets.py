from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib import pyplot
from matplotlib.patches import Patch
import numpy
import matplotlib
from .ColorPalette import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class BarChart(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        pyplot.style.use(['dark_background'])
        matplotlib.use('Qt5Agg')
        self.fig = Figure()
        FigureCanvasQTAgg.__init__(self, self.fig)

    def Plot(self, data, title, xLabel, yLabel):
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.title = title
        self.UpdatePlot(data)

    def UpdatePlot(self, data):
        xMin = 1-len(data[0])
        yMax = int(max(data[0]) * 1.2)
        ax = self.fig.add_subplot(111)
        ax.clear()
        ax.set_xlabel(self.xLabel)
        ax.set_ylabel(self.yLabel)
        ax.set_title(self.title)

        # Plot bar chart
        #ax.plot(range(xMin, 1), data[0])
        bars = ax.bar(range(xMin, 1), data[0],
                      width=1, align='edge', linewidth=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_color('gray')
        ax.spines['left'].set_bounds((0, yMax))
        ax.spines['bottom'].set_bounds((xMin, 0))
        ax.set_xlim(left=xMin, right=0)
        ax.set_ylim(bottom=0, top=yMax)

        # Color bars
        myInt = 0
        for patch in bars.patches:
            patch.set_facecolor(UIColors(data[1][myInt]))
            myInt = myInt + 1
        # Setup legend
        legendElements = []
        for i in range(len(UIColor)):
            if (i in data[1]):
                legendElements.append(Patch(facecolor = UIColors(i), linewidth = 0, label = ColorToDescription(UIColors(i))))
        ax.legend(handles=legendElements)
        # Draw grid and update
        ax.get_yaxis().grid(True, 'major', clip_on=True, ls='solid', lw=0.5, color='gray')

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
