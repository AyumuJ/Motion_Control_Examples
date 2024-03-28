"""
kpc101_pythonnet
==================

An example of using the .NET API with the pythonnet package for controlling a KPC101
Created on 2024-02-13 by Ayumu Ishijima
"""
#%%
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
#%%
def main():
    """The main entry point for the application"""

    # Uncomment this line if you are using
    # SimulationManager.Instance.InitializeSimulations()

    try:
        DeviceManagerCLI.BuildDeviceList()

        # create new device
        serial_no = "113250030"  # Replace this line with your device's serial number
        # serial_no = "113000001"  # For simulation

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

        # Load the device configuration
        device_config = device.GetPiezoConfiguration(serial_no)

        # This shows how to obtain the device settings
        device_settings = device.PiezoDeviceSettings

        # Set the Zero point of the device
        print("Setting Zero Point")
        device.SetZero()
        time.sleep(10.0) # Wait for device to set zero. Added by Ishijima

        # Get the maximum voltage output of the KPZ
        max_voltage = device.GetMaxOutputVoltage()  # This is stored as a .NET decimal
        max_travel = device.GetMaxTravel()  # This is stored as a .NET decimal
        print(f'Device max voltage is {max_voltage}')
        print(f'Device max travel is {max_travel}')

        # Go to a position
        dev_position = Decimal(10.0)
        print(f'Going to position {dev_position}')
        # # Go to a voltage
        # dev_voltage = Decimal(1.0)
        # print(f'Going to voltage {dev_voltage}')        

        if dev_position != Decimal(0) and dev_position <= max_travel:
            device.SetPosition(dev_position)
            print(f'Device position is {dev_position}')
            time.sleep(10.0)

            print(f'Moved to Position {device.GetPosition()}')
        else:
            print(f'Position must be between 0 and {max_travel}')

        # if dev_voltage != Decimal(0) and dev_voltage <= max_voltage:
        #     device.SetOutputVoltage(dev_voltage)
        #     print(f'Device voltage is {dev_voltage}')
        #     time.sleep(1.0)

        #     print(f'Moved to Voltage {device.GetOutputVoltage()}')
        # else:
        #     print(f'Voltage must be between 0 and {max_voltage}')

        # Stop Polling and Disconnect
        device.StopPolling()
        device.Disconnect()
    except Exception as e:
        print(e)

    # Uncomment this line if you are using Simulations
    # SimulationManager.Instance.UninitializeSimulations()
    ...


if __name__ == "__main__":
    main()

# %%
