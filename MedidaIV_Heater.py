#!/usr/bin/env python3
import csv
import sys
import os
import os.path
import pyvisa
import time
from datetime import datetime
import numpy as np
from subprocess import Popen,PIPE
import matplotlib.pyplot as plt
import pandas as pd

%matplotlib qt5

from KeysightB2902B import KeysightB2902B

#######################

min_V = 0.1
max_V = 1
step_V = 0.1
#steps_V = 30

time_interval_voltage = 1# Seconds

time_interval_average = 0.001 #Seconds

average_steps = 30

####2###################

def main():

    myKeysight = KeysightB2902B()
    myKeysight.KeysightB2902B_Connect("TCPIP::10.0.6.167::inst0:INSTR",1,10000,0)
    myKeysight.KeysightB2902B_SelectChannel(1)
    myKeysight.KeysightB2902B_OutputStatus(True,False)
    
    myKeysight.KeysightB2902B_SetCurrentLimit(1500./1e3)
    
    timestr = time.strftime("%Y%m%d-%H%M%S")

    voltage_range = myKeysight.KeysightB2902B_GetVoltageRange()
    current_range = myKeysight.KeysightB2902B_GetCurrentRange()

    current = []
    current_err = []
    time_a = []
    temp = []
    resistance = []
    #input_voltage = list(np.logspace(min_V,max_V,steps_V))
    input_voltage = list(np.arange(min_V,max_V,step_V))

    for voltage in input_voltage:
        myKeysight.KeysightB2902B_SetVoltage(voltage)
        time.sleep(time_interval_voltage)
        current_avg = 0.
        current_std = 0.

        for iCount in range(0,average_steps):
            #time.sleep(time_interval_average)
            iCurrent = float(myKeysight.KeysightB2902B_MeasureCurrent())
            current_avg += iCurrent
            current_std += iCurrent*iCurrent

        current_avg /= average_steps
        current.append(current_avg)

        current_std = np.sqrt(current_std/average_steps-current_avg*current_avg)/np.sqrt(average_steps)
        current_err.append(current_std)
        
        current_resistance = voltage/current_avg
        resistance.append(current_resistance)
        
        current_time = datetime.now().strftime("%H:%M:%S")
        time_a.append(current_time)
        
        print(current_avg, current_std,voltage, current_time)

    # df = pd.DataFrame({'Voltage':input_voltage})
    # df['Current'] = current
    # df['Current Error'] = current_err
    # df['Time'] = time_a
    # # df['Temperature'] = temp

    # print(df)

    #write data to file
    f = open(("%s_IV.txt" % timestr), "a")
    f.write("%s\t%f\n" %  ("Intervalo entre mediciones",time_interval_voltage))
    f.write("%s,%s,%s,%s,%s\n" % ("Voltage","Current","Current_Error","Resistance","Time"))
    for ii in range(0,len(input_voltage)):
        f.write("%f,%f,%f,%f,%s\n" % (input_voltage[ii],current[ii],current_err[ii],resistance[ii],time_a[ii]))
    f.close()

    #create plot
    fig, ax = plt.subplots()
    ax.scatter(x=input_voltage,y=current)
    ax.set_xlabel("Tensión [V]")
    ax.set_ylabel("Corriente [A]")
    fig.savefig(("%s_Heater_IV.png" % timestr))
    fig.show()

    fig, ax = plt.subplots()
    ax.scatter(x=input_voltage,y=current_err)
    ax.set_xlabel("Tensión [V]")
    ax.set_ylabel("Desvio Corriente [A]")
    fig.savefig(("%s_Heater_IV.png" % timestr))
    fig.show()
    
    fig, ax = plt.subplots()
    ax.scatter(input_voltage,resistance)
    ax.set_xlabel("Tensión [V]")
    ax.set_ylabel("R [$\Omega$]")
    fig.savefig(("%s_Heater_RV.png" % timestr))
    fig.show()
    
    
    #myKeysight.KeysightB2902B_SetVoltage(0.)

    #myKeysight.KeysightB2902B_Disconnect()



if __name__ == "__main__":
        main()
