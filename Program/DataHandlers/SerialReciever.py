import serial
import statistics
import pandas as pd
import numpy as np
import scipy.signal
import vector
import matplotlib.pyplot as plt
from datetime import datetime as dt
class SerialReceiver:
    def __init__(self):
        self.ser = serial.Serial(port = 'COM9', baudrate = 9600, timeout = 0.1)
        self.ser.flushInput()
        self.dataFrame = pd.DataFrame(columns = ['RRData', 'Time'])
        self.minuteCounter = 0
        self.hourCounter = 0
        self.dayCounter = 0
        #dataFrame = pd.DataFrame(columns = ['RRData'])

    #can we make the python dataFrame2 run and append to 15 seconds worth of data
    #and then calculate respriatory rate over that and append it to the first df?
    @staticmethod
    def RemoveFromList(the_list, val):
        [value for value in the_list if value != val]

    def Get_RR(self, list_input, window = None):
        #RRlist = []
        #for item in products_list:
            #RRlist.append(item)
        #print(products_list)
        #meanAnalogValue = dataFrame.mean()
        #print("mean analog value is... " + meanAnalogValue)
        RRlist2 = []
        self.RemoveFromList(list_input, '')
        for item in list_input:
            RRlist2.append(int(item))
        floatingMean = statistics.mean(RRlist2)
        integerMean = int(round(floatingMean))
        print("rounded mean is... " + str(integerMean))
        vector = np.array(RRlist2)
        indexes, _ = scipy.signal.find_peaks(vector, height=60, distance=35)
        print('Peaks indexes: %s' % (indexes))

        # plot the values and their peaks marked with 'x'
        #plt.plot(vector)
        #plt.plot(indexes, vector[indexes], "x")
        #plt.plot(np.zeros_like(vector), "--", color = "gray")
        #plt.show()
        
        # find values of the peaks and store them    
        peak_values = []
        for index in indexes:
            value = RRlist2[index]
            peak_values.append(value)
        #print('Actual peak values: %s' % (peak_values))
        respiratoryRate = len(peak_values)
        #print('Respiratory Rate: ' + str(respiratoryRate))
        if (window != None):
            window.SetData(respiratoryRate)
        #print(RRlist2)
    def GetSerial(self, window = None):
        while True:
            try:
                ser_bytes = self.ser.readline()
                decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                now = dt.now()
                current_time = now.strftime("%H:%M:%S.%f")[:-3]
                data = [decoded_bytes, current_time]
                #dataFrame2 = pd.DataFrame([decoded_bytes, current_time], columns = ['RRData', 'Time'])
                dataFrame2 = pd.DataFrame([data], columns = ['RRData', 'Time'])
                self.dataFrame = self.dataFrame.append(dataFrame2)

                #minute chart RR calculations
                #20 serial reads per second, or 1200 per minute
                minuteDataFrame = pd.DataFrame(columns = ["RRData"])
                if self.minuteCounter < 1200:
                    minuteDataFrame2 = pd.DataFrame([decoded_bytes], columns = ["RRData"])
                    minuteDataFrame = minuteDataFrame.append(minuteDataFrame2)
                    print(self.minuteCounter, decoded_bytes)
                    self.minuteCounter = self.minuteCounter + 1
                else: #this is when the minutecounter will equal to one minute of data gathered
                    # do the one minute fourier transform with data from minuteDataFrame
                    # store the RR datapoint (actual respiratory rate) somewhere and plot it!
                    # calculate the average, then how many times the sine wave crosses the avg
                    # then get the RR from that
                    # also reset the minuteCounter variable to 0
                    RR_list = self.dataFrame["RRData"].tolist()
                    self.Get_RR(RR_list, window)
                    self.minuteCounter = 0
                    
                #print(decoded_bytes)
            except KeyboardInterrupt:
                print("datalogging interrupted")
                pd.set_option("display.max_rows", None, "display.max_columns", None)
                print(self.dataFrame)
                break
        
if __name__ == "__main__":
    sr = SerialReceiver()
    sr.GetSerial()

# define a function that takes in a dataframe, then creates an empty queue out of it
# then calculates the average of that queue
