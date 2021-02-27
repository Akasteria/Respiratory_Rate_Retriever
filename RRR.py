import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Tools import Pseudodata
from Widgets import LineChart
def main():
    # TODO take inputs from bluetooth
    # data = 
    
    # Drawing GUI
    app = QApplication()
    lc = LineChart.LineChart(Pseudodata.GenerateSet(31, 30, 10, 20, 17), 30, 'Time (s)', 'Respiration Rate', 'Past Hour',10,10,500,500)
    win = lc.widget
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()