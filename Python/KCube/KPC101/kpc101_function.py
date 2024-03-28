"""
kpc101_function.py
==================
An example of using the .NET API with the pythonnet package for controlling a KPC101
Created on 2024-03-28 by Ayumu Ishijima
"""
import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericPiezoCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.PiezoStrainGaugeCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericPiezoCLI import *
from Thorlabs.MotionControl.KCube.PiezoStrainGaugeCLI import *
from System import Decimal  # necessary for real world units

def kpc101_initialize(serial_no):
    try:
        DeviceManagerCLI.BuildDeviceList()

        # Connect, begin polling, and enable
        device = KCubePiezoStrainGauge.CreateKCubePiezoStrainGauge(serial_no)
        device.Connect(serial_no)

        # Get Device Information and display description
        device_info = device.GetDeviceInfo()
        print(device_info.Description)

        # Start polling and enable
        device.StartPolling(250)  #250ms polling rate
        time.sleep(25)
        device.EnableDevice()
        time.sleep(0.25)  # Wait for device to enable

        if not device.IsSettingsInitialized():
            device.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert device.IsSettingsInitialized() is True

        device_config = device.GetPiezoConfiguration(serial_no) # Load the device configuration
        device_settings = device.PiezoDeviceSettings # This shows how to obtain the device settings
        
        # Get the maximum voltage output of the KPZ
        max_voltage = device.GetMaxOutputVoltage()  # This is stored as a .NET decimal
        max_travel = device.GetMaxTravel()  # This is stored as a .NET decimal
        print(f'Device max voltage is {max_voltage}')
        print(f'Device max travel is {max_travel}')
    except Exception as e:
        print(e)
    return device, max_travel

def kpc101_SetZero(device):
    # Set the Zero point of the device
    print("Setting Zero Point")
    device.SetZero()
    time.sleep(6.0) # Wait for device to set zero. Added by Ishijima
    
def kpc101_move(device,max_travel,x):
    # Go to a position
    dev_position = x    
    if dev_position != Decimal(0) and dev_position <= max_travel:
        device.SetPosition(dev_position)
        time.sleep(0.5)
        print(f'Moved to Position {device.GetPosition()}')
    else:
        print(f'Position must be between 0 and {max_travel}')

def kpc101_close(device):
    # Stop Polling and Disconnect
    device.StopPolling()
    device.Disconnect()
    print("Disconnected from device")

#%%
serial_no = "113250030"  # Replace this line with your device's serial number
step = 1 #um
scan_width = 10.0 #um
center_position = 10.0 #um
device, max_travel = kpc101_initialize(serial_no)
kpc101_move(device,max_travel,x=Decimal(center_position))
print(f'Current position is {device.GetPosition()}')
start_position = device.GetPosition() - Decimal(scan_width/2.0)
if start_position < Decimal(0):
    print("Start position is less than 0. Change the scan width.")
    kpc101_close(device)

for i in range(0, int(scan_width/step)+1):
    x = start_position + Decimal(i*step)
    kpc101_move(device,max_travel,x)
    time.sleep(2)

kpc101_close(device)