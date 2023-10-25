# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 16:01:46 2023

@author: juancosta
"""

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

# DEFINICIONES
#######################

#TIEMPO

time_steps = 2000

#TENSION
time_interval_voltage = 20# Seconds
voltage = 3.3

#PROMEDIACIÓN
average_steps = 3

#########################
# NO TOCAR
############################

#######################

def current_mili_time():
    return round(time.time()*1000)

def main():
    
    print(time_steps)

    if(time_steps<0):
        exit()
    
    myKeysight = KeysightB2902B()
    myKeysight.KeysightB2902B_Connect("TCPIP::10.0.6.167::inst0:INSTR",1,10000,0)
    myKeysight.KeysightB2902B_SelectChannel(1)
    
    myKeysight.KeysightB2902B_SetVoltage(0)
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

    myKeysight.KeysightB2902B_SetVoltage(0)
    
   # time.sleep(time_interval_voltage)
    
    myKeysight.KeysightB2902B_SetVoltage(voltage)
    
    initial_time = current_mili_time()
    
    for i in range(time_steps):
        current_avg = 0.
        current_std = 0.
        
        for iCount in range(0,average_steps):
            iCurrent = float(myKeysight.KeysightB2902B_MeasureCurrent())
            current_avg += iCurrent
            current_std += iCurrent*iCurrent

        current_avg /= average_steps
        current.append(current_avg)

        current_std = np.sqrt(current_std/average_steps-current_avg*current_avg)/np.sqrt(average_steps)
        current_err.append(current_std)
        
        current_resistance = voltage/current_avg
        resistance.append(current_resistance)
        
        current_time = (current_mili_time()-initial_time)/1000
        time_a.append(current_time)
        
        print(current_avg, current_std,voltage, current_time)
    
    myKeysight.KeysightB2902B_SetVoltage(0)

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
    for ii in range(0,len(time_a)):
        f.write("%f,%f,%f,%f,%s\n" % (voltage,current[ii],current_err[ii],resistance[ii],time_a[ii]))
    f.close()

    #create plot
    fig, ax = plt.subplots()
    ax.scatter(x=time_a,y=current_err)
    ax.set_xlabel("Tensión [V]")
    ax.set_ylabel("Desvio Corriente [A]")
    fig.savefig(("%s_Heater_IT.png" % timestr))
    fig.show()
    
    fig, ax = plt.subplots()
    ax.scatter(time_a,resistance)
    ax.set_xlabel("Tensión [V]")
    ax.set_ylabel("R [$\Omega$]")
    fig.savefig(("%s_Heater_RT.png" % timestr))
    fig.show()
    
    
    #myKeysight.KeysightB2902B_SetVoltage(0.)

    #myKeysight.KeysightB2902B_Disconnect()



if __name__ == "__main__":
        main()