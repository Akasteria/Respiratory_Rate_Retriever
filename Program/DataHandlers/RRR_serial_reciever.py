import serial
import statistics
import pandas as pd
import numpy as np
import scipy.signal
import vector
import matplotlib.pyplot as plt
from datetime import datetime as dt

ser = serial.Serial(port = 'COM3', baudrate = 9600, timeout = 0.1)
ser.flushInput()
dataFrame = pd.DataFrame(columns = ['RRData', 'Time'])
#dataFrame = pd.DataFrame(columns = ['RRData'])

#can we make the python dataFrame2 run and append to 15 seconds worth of data
#and then calculate respriatory rate over that and append it to the first df?

def removeFromList(the_list, val):
    [value for value in the_list if value != val]


def get_RR(list_input):
    #RRlist = []
    #for item in products_list:
        #RRlist.append(item)
    #print(products_list)
    #meanAnalogValue = dataFrame.mean()
    #print("mean analog value is... " + meanAnalogValue)
    RRlist2 = []
    removeFromList(list_input, '')
    for item in list_input:
        if item in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    '10', '11', '12', '13', '14', '15', '16', '17', '18',
                    '19', '20', '21', '22', '23', '24', '25', '26', '27',
                    '28', '29', '30', '31', '32', '33', '34', '35', '36',
                    '37', '38', '39', '40', '41', '42', '43', '44', '45',
                    '46', '47', '48', '49', '50', '51', '52', '53', '54',
                    '55', '56', '57', '58', '59', '60', '61', '62', '63',
                    '64', '65', '66', '67', '68', '69', '70', '71', '72',
                    '73', '74', '75', '76', '77', '78', '79', '80', '81',
                    '82', '83', '84', '85', '86', '87', '88', '89', '90',
                    '91', '92', '93', '94', '95', '96', '97', '98', '99',
                    '100', '-1', '-2', '-3', '-4', '-5', '-6', '-7', '-8']:
            RRlist2.append(int(item))
    floatingMean = statistics.mean(RRlist2)
    integerMean = int(round(floatingMean))
    print("rounded mean is... " + str(integerMean))
    vector = np.array(RRlist2)
    indexes, _ = scipy.signal.find_peaks(vector, height=60, distance=35)
    print('Peaks indexes: %s' % (indexes))

    # plot the values and their peaks marked with 'x'
    plt.plot(vector)
    plt.plot(indexes, vector[indexes], "x")
    plt.plot(np.zeros_like(vector), "--", color = "gray")
    plt.show()
    
    # find values of the peaks and store them    
    peak_values = []
    for index in indexes:
        value = RRlist2[index]
        peak_values.append(value)
    print('Actual peak values: %s' % (peak_values))
    respiratoryRate = len(peak_values)
    print('Respiratory Rate: ' + str(respiratoryRate))

    #print(RRlist2)
minuteCounter = 0
hourCounter = 0
dayCounter = 0

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
        minuteDataFrame = pd.DataFrame(columns = ["RRData"])
        if minuteCounter < 1200:
            minuteDataFrame2 = pd.DataFrame([decoded_bytes], columns = ["RRData"])
            minuteDataFrame = minuteDataFrame.append(minuteDataFrame2)
            print(minuteCounter, decoded_bytes)
            minuteCounter = minuteCounter + 1
        else: #this is when the minutecounter will equal to one minute of data gathered
            # do the one minute fourier transform with data from minuteDataFrame
            # store the RR datapoint (actual respiratory rate) somewhere and plot it!
            # calculate the average, then how many times the sine wave crosses the avg
            # then get the RR from that
            # also reset the minuteCounter variable to 0
            RR_list = dataFrame["RRData"].tolist()
            get_RR(RR_list)
            minuteCounter = 0
            break
            
            
        #print(decoded_bytes)
    except KeyboardInterrupt:
        print("datalogging interrupted")
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(dataFrame)
        break
        


# define a function that takes in a dataframe, then creates an empty queue out of it
# then calculates the average of that queue
