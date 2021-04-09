import Program.RRR as RRR
import os
import sys
with open(os.path.join(sys.path[0],'styleSheet.txt')) as sheet:
    window = RRR.ShowGUI(sheet.read())
    while True:
        data = input("New data:")
        window.SetData(data)
        

# TODO do data analysis