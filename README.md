# Dust_BlastGate

This project is a Dust collection system blast gate for woodworking or other dust collection.  The device provides control of a servo to actuate the blast gate, manual control of the blast gate position, a connector to attatch a sensor for tool activation and automatic control and wifi connection to activate a dust collector connected to a Kassa capable smart plug or switch.  

Software is seetup to allow over the air firmware updates direct from github. BoardInfo.py and Settings.py are not part of OTA update. BoardInfo.py contains hardware pinouts and should reflect hardware revisions.  Settings.py contains device configurations, i.e. wifi, servo limits, IP for dust collector and delay time.  These settings are set per device

BoardInfo files contain board specific information (i.e. pin mappings), BoardInfo must be loaded manualy at inital install and will not update OTA.  

Hardware folder contains KiCAD files for board revisions.  Boards are uploaded to OSHpark.  

Firmware folder contains the firmware.  Files except Settings.py are subject to OTA update.  

settings.py file contains example data/startup data. File will be overwritten when configuring board for the first time.  Write this file durring intial install.

OTA updated based on MicroPython OTA Updater (https://github.com/rdehuyss/micropython-ota-updater#micropython-ota-updater)
KASA integration based on the work by 