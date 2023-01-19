##Import libraries

import machine
try:
  import usocket as socket
except:
  import socket
import network
import time
from struct import pack

#BoardInfo.py contains hardware specific information (i.e. pinouts, constant per hardware revision but may change with upddated hardware
import BoardInfo
#Settings.py containd device specific informaton (i.e. wifi configuration, open and closed positions and delay time)
import Settings

#define Variables - grab data from Settings.py configuration file
SSID = Settings.SSID
password = Settings.password
DCIP= Settings.DCIP
closedPos=Settings.closedPos
openPos= Settings.openPos
delayTime=Settings.delayTime
delay2=Settings.delay2



#define functions
def connectWIFI():
    WIFI.active(True)
    for i in range(0,150):
        print(WIFI.isconnected())
        if WIFI.isconnected():
            print("WIFI is connected")
            break
        else:
            print("Trying to connect " + str(i))
            try:
                WIFI.connect(SSID, password)
            except:
                if i % 20 == 0:
                    WIFI.active(False)
                    time.sleep_ms(10)
                    WIFI.active(True)
            for x in range(0,5):
                time.sleep(1)
                if WIFI.isconnected():
                    break        
            
def servoSet(pos):
    #sets servo, to value between 0 and 100
    posA = min(max(0, pos),100)
    outval=int(posA*.75)+40
    servo.duty(outval)
    #print(outval)        

def TurnOnDC():
    servoSet(openPos)
    print("Open")
    SetPlug('{"system":{"set_relay_state":{"state":1}}}')


def TurnOffDC():

    SetPlug('{"system":{"set_relay_state":{"state":0}}}')
    for x in range(0,20):   
        if getStatus():
            SetPlug('{"system":{"set_relay_state":{"state":0}}}')    
    time.sleep(delay2)
    servoSet(closedPos)
    print("Closed")



def SetPlug(cmd):
    if wifiEnP():
            
        if WIFI.isconnected():
            print("WIFI is connected, sending comand to Dust Collector")
            try:
                s = socket.socket()
                s.settimeout(100)
                addr = socket.getaddrinfo(DCIP, 9999)[0][-1]
                s.connect(addr)
                encrypted = encrypt(cmd)
                s.send(encrypted)
                s.close
            except:
                print("Error sendingn to DC")
           
def getStatus():
    try:
        s = socket.socket()
        s.settimeout(100)
        addr = socket.getaddrinfo(DCIP, 9999)[0][-1]
        s.connect(addr)
        encrypted = encrypt('{"system":{"get_sysinfo":{}}}')
        s.send(encrypted)
        data = s.recv(2048)
        s.close
        decrypted = decrypt(data[4:])
        data = decrypted.split(',')
        for d in data:
            stat=d.split(":")
    #         print(stat[0] , stat[1])
    #         print(stat[1])
            if stat[0] == '"relay_state"':
    #             print(stat[0])
    #             print(stat[1])
                return stat[1]
    except:
        print("Error getting Status")

def encrypt(string):
    key = 171
    result = pack(">I", len(string))
    for i in string:
        a = key ^ ord(i)
        key = a
        result += bytes([a])
    return result

def decrypt(string):
    key = 171
    result = ""
    for i in string:
        a = key ^ i
        key = i
        result += chr(a)
    return result


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
            for i in range (0,5):
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
    else :
        on = False
