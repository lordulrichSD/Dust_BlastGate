##Import libraries

import machine
try:
  import usocket as socket
except:
  import socket
import network
import time
from struct import pack
import gc

#BoardInfo.py contains hardware specific information (i.e. pinouts, constant per hardware revision but may change with upddated hardware
import BoardInfo
#Settings.py containd device specific informaton (i.e. wifi configuration, open and closed positions and delay time)
import Settings

gc.enable()

#define Variables - grab data from Settings.py configuration file
SSID = Settings.SSID
password = Settings.password
DCIP= Settings.DCIP
closedPos=Settings.closedPos
openPos= Settings.openPos
delayTime=Settings.delayTime
delay2=Settings.delay2



#define functions


#Setup pins
#setup pins
modeP = machine.Pin(BoardInfo.modePin, machine.Pin.IN)      
senseP =  machine.Pin(BoardInfo.sensePin, machine.Pin.IN)
manOnP = machine.Pin(BoardInfo.manOnPin, machine.Pin.IN)
manOffP = machine.Pin(BoardInfo.manOffPin, machine.Pin.IN)
wifiEnP = machine.Pin(BoardInfo.wifiEnPin, machine.Pin.IN)
senseEnP = machine.Pin(BoardInfo.senseEnPin, machine.Pin.IN)


#Led pins, set to off
dcStatusP = machine.Pin(BoardInfo.dcStatusPin, machine.Pin.OUT)
dcStatusP.value(0)

senseStatusP = machine.Pin(BoardInfo.senseStatusPin, machine.Pin.OUT)
senseStatusP.value(0)

wifiStatusP = machine.Pin(BoardInfo.wifiStatusPin, machine.Pin.OUT)
wifiStatusP.value(0)

##Check Mode
if (modeP.value()==1):
    import APmode
    APmode.run()


#setup sero
servoP=machine.Pin(BoardInfo.servoPin, machine.Pin.OUT)
servo = machine.PWM(servoP,freq=50)
print("closing servo")
servoSet(closedPos)

if wifiEnP():
    #check if WIFI Enabled and if so try to connect    
    WIFI = network.WLAN(network.STA_IF)
    connectWIFI()
    wifiStatusP.value(WIFI.isconnected())


on=False

#Go to loop
while (True):
    if wifiEnP():
        if WIFI.isconnected():
            wifiStatusP.value(1)
            #print("DC Status Value")
            #print(getStatus())
            if getStatus() == "1":
                dcStatusP.value(1)
                print("Dust Collector On")
            else:
                dcStatusP.value(0)
                print("Dust Collector Off")
        else:
            connectWIFI()
            wifiStatusP.value(WIFI.isconnected())
    
    #Sense operating position
    if manOnP.value():
        #Manual On
        print("Manual On")
        #if on==False:
        TurnOnDC()          
        on = True

    elif manOffP.value():
        print("Manual Off")
        if on==True:
            time.sleep(delayTime)
            TurnOffDC()
                
        on = False
        
    elif senseEnP.value():
        print("Auto Sense")
        
        if senseP.value():
            print("Auto On")
            senseStatusP.value(1)
            #if on==False:
            TurnOnDC()          
            on = True
        else:
            print("Auto Off")
            senseStatusP.value(0)
            if on==True:
                time.sleep(delayTime)
                TurnOffDC()
            on = False           

    gc.collect()
    time.sleep_ms(10)
    