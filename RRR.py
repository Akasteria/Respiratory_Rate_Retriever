import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Tools import Pseudodata
from Widgets import MyWidgets
from Widgets import CompositeWidgets
def main():
    # TODO take inputs from bluetooth
    # data = 
    
    # Drawing GUI
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget {background-color: black}")
    data = Pseudodata.GenerateSet(61,(15,18),False, None, (25,30))
    data2 = Pseudodata.GenerateSet(25,(15,18),True,(20,24), (25,30))
    data3 = Pseudodata.GenerateSet(8,(15,18),False)
    window = CompositeWidgets.ChartValuePairList(data,data2,data3)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()