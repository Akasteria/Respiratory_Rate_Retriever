import Program.RRR as RRR
import os
import sys
from Program.DataHandlers.SerialReceiver import SerialReceiver
with open(os.path.join(sys.path[0],'styleSheet.txt')) as sheet:
    RRR.GUI(sheet.read())
