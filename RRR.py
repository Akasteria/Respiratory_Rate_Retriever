import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Tools import Pseudodata
from Widgets import MyWidgets
def main():
    # TODO take inputs from bluetooth
    # data = 
    
    # Drawing GUI
    app = QApplication(sys.argv)
    lc = MyWidgets.LineChart()
    lc.Plot(Pseudodata.GenerateSet(61,(15,18),True,(20,24), (25,30)),'Past Hour','Time (min)', 'Respiration Rate')
    #lc.show()
    window = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(lc)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()