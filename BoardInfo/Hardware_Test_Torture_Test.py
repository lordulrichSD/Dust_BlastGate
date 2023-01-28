#Code to test power consumption of board in max load

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

#setup pins
modeP = machine.Pin(BoardInfo.modePin, machine.Pin.IN)      
senseP =  machine.Pin(BoardInfo.sensePin, machine.Pin.IN)
manOnP = machine.Pin(BoardInfo.manOnPin, machine.Pin.IN)
manOffP = machine.Pin(BoardInfo.manOffPin, machine.Pin.IN)
wifiEnP = machine.Pin(BoardInfo.wifiEnPin, machine.Pin.IN)
senseEnP = machine.Pin(BoardInfo.senseEnPin, machine.Pin.IN)



#Led pins, set to off
dcStatusP = machine.Pin(BoardInfo.dcStatusPin, machine.Pin.OUT)
dcStatusP.value(1)

progP= machine.Pin(13, machine.Pin.OUT)
progP.value(1)

senseStatusP = machine.Pin(BoardInfo.senseStatusPin, machine.Pin.OUT)
senseStatusP.value(1)

wifiStatusP = machine.Pin(BoardInfo.wifiStatusPin, machine.Pin.OUT)
wifiStatusP.value(1)


#Setup network connection
import network
import machine
update=False
uid=machine.unique_id()
Device=''.join(['{:02x}'.format(b) for b in uid])
AP="BlastGate_"+Device
print("Starting AP")
ap=network.WLAN(network.AP_IF)
ap.active(False)
ap.active(True)
ap.config(essid=AP, password='12345')



try:
    import usocket as socket
except:
    import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)



while True:
    TurnOnDC()
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    strrequest=str(request)
    print(strrequest)
    ispost=strrequest.startswith("b'POST")
    print(ispost)
    if (ispost):
        print("process POST request")

    html = webpage(SSID, password, DCIP, closedPos, openPos, delayTime)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(html)
    conn.close()    
    TurnOffDC()