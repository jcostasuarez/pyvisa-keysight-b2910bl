#!/usr/bin/env python3

import pyvisa
import socket
import time


class KeysightB2902B:
    
    def __init__(self):
        #global variables
        self._rm              = pyvisa.ResourceManager('@py')
        self._my_daq          = None
        self._out_channel_id  = -1
        self._channelON       = [False,False]


    def ShowResources(self):
        print(self._rm.list_resources())

    def KeysightB2902B_Connect(self,rsrcString, getIdStr, timeout, doReset):

        #self._my_daq = self._rm.open_resource("USB0::10893::37377::MY61390786::0::INSTR")
        self._my_daq = self._rm.open_resource(rsrcString)

        self._my_daq.write_termination = '\n'
        self._my_daq.read_termination = '\n'

        self._my_daq.timeout = timeout

        if getIdStr == 1: 
            print(self._my_daq.query("*IDN?"))
            time.sleep(0.3)

        if doReset == 1:
            self._my_daq.write('*RST')
            time.sleep(0.3)
        
        return self._my_daq

    def KeysightB2902B_Disconnect(self):
        self.KeysightB2902B_OutputStatus(False,False) #disable output if not already done
        self._my_daq.close()
        print("DAQ connection closed")
        return

    def KeysightB2902B_SelectChannel(self,myChan):
        self._out_channel_id = myChan
        return

    def checkChannelStatus(self):
        if not(self._out_channel_id==1 or self._out_channel_id==2):
            print("ERROR! Channel ID [",self._out_channel_id,"] is not possible")
            print("Diconnecting")
            KeysightB2902B_Disconnect()
        return

    def KeysightB2902B_SetVoltage(self,volt): #units are in 'V'
        self.checkChannelStatus()
        self._my_daq.write(':SOUR%d:FUNC:MODE VOLT' %self._out_channel_id)
        self._my_daq.write(':SOUR%d:VOLT %G' % (self._out_channel_id,volt))
        if not(self._channelON[self._out_channel_id-1]): print("Warning! Channel ",self._out_channel_id," has not been switched on")

    def KeysightB2902B_SetVoltageLimit(self,volt_limit):  #units are in 'V'
        self.checkChannelStatus()
        self._my_daq.write(':SENS%d:FUNC:MODE VOLT' %self._out_channel_id)
        self._my_daq.write(':SENS%d:VOLT:PROT %G' % (self._out_channel_id,volt_limit))


    def KeysightB2902B_MeasureVoltage(self): #units are in 'V'
        self.checkChannelStatus()
        if not(self._channelON[self._out_channel_id-1]): print("Warning! Channel ",self._out_channel_id," has not been switched on")

        return self._my_daq.query(':MEAS:VOLT? (@%d)' %self._out_channel_id)    
    
    def KeysightB2902B_GetVoltageRange(self): #units are in 'V'
        self.checkChannelStatus()
        if not(self._channelON[self._out_channel_id-1]): print("Warning! Channel ",self._out_channel_id," has not been switched on")

        return self._my_daq.query(':SOUR:VOLT:RANG?')

    def KeysightB2902B_GetCurrentRange(self): #units are in 'V'
        self.checkChannelStatus()
        if not(self._channelON[self._out_channel_id-1]): print("Warning! Channel ",self._out_channel_id," has not been switched on")

        return self._my_daq.query(':SOUR:CURR:RANG?')

    def KeysightB2902B_SetVoltageRange(self,volt): #units are in 'V'
        self.checkChannelStatus()
        if not(self._channelON[self._out_channel_id-1]): print("Warning! Channel ",self._out_channel_id," has not been switched on")

        return self._my_daq.query(':SOUR:VOLT:RANG %G' % volt)

    def KeysightB2902B_SetCurrentRange(self,curr): #units are in 'V'
        self.checkChannelStatus()
        if not(self._channelON[self._out_channel_id-1]): print("Warning! Channel ",self._out_channel_id," has not been switched on")

        return self._my_daq.query(':SOUR:CURR:RANG %G' % curr)


    def KeysightB2902B_SetCurrent(self,current): #units are in 'A'
        self.checkChannelStatus()
        self._my_daq.write(':SOUR%d:FUNC:MODE CURR' %self._out_channel_id)
        self._my_daq.write(':SOUR%d:CURR %G' % (self._out_channel_id,volt))
        if not(self._channelON[self._out_channel_id-1]): print("Warning! Channel ",self._out_channel_id," has not been switched on")

    def KeysightB2902B_SetCurrentLimit(self,current_limit):  #units are in 'A'
        self.checkChannelStatus()
        self._my_daq.write(':SENS%d:FUNC:MODE CURR' %self._out_channel_id)
        self._my_daq.write(':SENS%d:CURR:PROT %G' % (self._out_channel_id,current_limit))

    def KeysightB2902B_MeasureCurrent(self): #units are in 'A'
        self.checkChannelStatus()
        if not(self._channelON[self._out_channel_id-1]): print("Warning! Channel ",self._out_channel_id," has not been switched on")

        return self._my_daq.query(':MEAS:CURR? (@%d)' %self._out_channel_id)
    

    def KeysightB2902B_OutputStatus(self,channel1=False,channel2=False):
        if(channel1): 
            self._my_daq.write(':OUTP1 ON')
            self._channelON[0] = True
        else:
            self._my_daq.write(':OUTP1 OFF')
            self._channelON[0] = False

        if(channel2): 
            self._my_daq.write(':OUTP2 ON')
            self._channelON[1] = True
        else:
            self._my_daq.write(':OUTP2 OFF')
            self._channelON[1] = False

