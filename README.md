# Dust_BlastGate

This project is a Dust collection system blast gate for woodworking or other dust collection.  The device provides control of a servo to actuate the blast gate, manual control of the blast gate position, a connector to attatch a sensor for tool activation and automatic control and wifi connection to activate a dust collector connected to a Kassa capable smart plug or switch.  

Software is seetup to allow over the air firmware updates direct from github. BoardInfo.py and Settings.py are not part of OTA update. BoardInfo.py contains hardware pinouts and should reflect hardware revisions.  Settings.py contains device configurations, i.e. wifi, servo limits, IP for dust collector and delay time.  These settings are set per device

BoardInfo files contain board specific information (i.e. pin mappings), BoardInfo must be loaded manualy at inital install and will not update OTA.  

Hardware folder contains KiCAD files for board revisions.  Boards are uploaded to OSHpark.  

Firmware folder contains the firmware.  Files except Settings.py are subject to OTA update.  

settings.py file contains example data/startup data. File will be overwritten when configuring board for the first time.  Write this file durring intial install.


Hardware
Hardware contains 2 main modules.  The main control module and sensor module.  
The main control module contains an ESP32 module (providing microcontroler and wifi connection).  In addition the main control module holds support hardware (i.e. power supply) and interface connections.  
A manual control switch (1p3t on-off-on) provides manual on, auto, manual off control.  
Dip switches provide for entering Access Point Mode for settings, enabling WIFI (when not in AP mode) enabling the sensor in put.  
A FTDI type 6 pin headder is provided for programing and debug by serial.
A 3 pin header is provided to connect a hobby servo to activate the physical blast gate
Sensor connection is via a RJ-9 Style connector to allow easy cable creation of needed lenght for indivitual physical install.  This connector includes 3.3v, ground, sensor data (logic high/low), and raw USB voltage (allowing USB power supply to be at sensor location)
A USB connetor is provided for power only.  A jumper or switch (populate 1) allowing selection of power source (one at a time, sensor or main control module)





(Future feature to deploy)
OTA updated based on MicroPython OTA Updater (https://github.com/rdehuyss/micropython-ota-updater#micropython-ota-updater)


KASA integration based on the work by GadgetReactor in the pyHS100 based on the work of The communication protocol was reverse engineered by Lubomir Stroetmann and
Tobias Esser in 'Reverse Engineering the TP-Link HS110':
https://www.softscheck.com/en/reverse-engineering-tp-link-hs110/.  The HS100 or python-kasa libraries were not used directly due to memory limitations of the ESP32 module so only limited functions were recreated directly.

