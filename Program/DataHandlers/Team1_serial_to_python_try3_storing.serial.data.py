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
        print(decoded_bytes)
    except KeyboardInterrupt:
        print("datalogging interrupted")
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(dataFrame)
        break
        
