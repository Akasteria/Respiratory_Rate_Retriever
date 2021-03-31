import Program.RRR as RRR
import os
import sys
with open(os.path.join(sys.path[0],'styleSheet.txt')) as sheet:
    RRR.ShowGUI(sheet.read())
# TODO do data analysis