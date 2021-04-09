import Program.RRR as RRR
import os
import sys
from Program.DataHandlers.SerialReciever import SerialReceiver
with open(os.path.join(sys.path[0],'styleSheet.txt')) as sheet:
    window = RRR.ShowGUI(sheet.read())
    sr = SerialReceiver()
    sr.GetSerial(window)

# TODO do data analysis