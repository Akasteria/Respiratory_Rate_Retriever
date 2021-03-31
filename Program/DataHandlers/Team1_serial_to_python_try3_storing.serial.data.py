import serial
import pandas as pd
import numpy as np
from datetime import datetime as dt

ser = serial.Serial(port = 'COM3', baudrate = 9600, timeout = 0.1)
ser.flushInput()
dataFrame = pd.DataFrame(columns = ['RRData', 'Time'])
#dataFrame = pd.DataFrame(columns = ['RRData'])

#can we make the python dataFrame2 run and append to 15 seconds worth of data
#and then calculate respriatory rate over that and append it to the first df?

while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        now = dt.now()
        current_time = now.strftime("%H:%M:%S.%f")[:-3]
        data = [decoded_bytes, current_time]
        #dataFrame2 = pd.DataFrame([decoded_bytes, current_time], columns = ['RRData', 'Time'])
        dataFrame2 = pd.DataFrame([data], columns = ['RRData', 'Time'])
        dataFrame = dataFrame.append(dataFrame2)

        #minute chart RR calculations
        #20 serial reads per second, or 1200 per minute
        minuteCounter = 0
        hourCounter = 0
        dayCounter = 0
        minuteDataFrame = pd.DataFrame(columns = ["RRData"])
        if minuteCounter < 1200:
            minuteDataFrame2 = pd.DataFrame([decoded_bytes], columns = ["RRData"])
            minuteDataFrame = minuteDataFrame.append(minuteDataFrame2)
            minuteCounter = minuteCounter + 1
        else: #this is when the minutecounter will equal to one minute of data gathered
            # do the one minute fourier transform with data from minuteDataFrame
            # store the RR datapoint (actual respiratory rate) somewhere and plot it!
            
            
        print(decoded_bytes)
    except KeyboardInterrupt:
        print("datalogging interrupted")
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(dataFrame)
        break
        
