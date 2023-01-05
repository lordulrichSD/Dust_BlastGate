#hardware test program for blast gate
#This program to test board assembly, will flaxh LEDs, run servo limit to limit and then print inputs to the serial port

import machine
import time

import BoardInfo


closedPos=0
openPos=100

def servoSet(pos):
    #sets servo, to value between 0 and 100
    posA = min(max(0, pos),100)
    outval=int(posA*.75)+40
    servo.duty(outval)
    #print(outval)     

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

progP= machine.Pin(13, machine.Pin.OUT)
progP.value(0)

senseStatusP = machine.Pin(BoardInfo.senseStatusPin, machine.Pin.OUT)
senseStatusP.value(0)

wifiStatusP = machine.Pin(BoardInfo.wifiStatusPin, machine.Pin.OUT)
wifiStatusP.value(0)

def lights(v):
    wifiStatusP.value(v)
    senseStatusP.value(v)
    dcStatusP.value(v)
    progP.value(v)

print("Blast Gate Hardware Test")
print("Servo Test - Servo Sweeps 10 Seconds")
#setup sero
servoP=machine.Pin(BoardInfo.servoPin, machine.Pin.OUT)
servo = machine.PWM(servoP,freq=50)

servoSet(closedPos)
for i in range(0,5):
    time.sleep(1)
    servoSet(openPos)
    time.sleep(1)
    servoSet(closedPos)
print("Servo Test Done")
print("Status Light Test - All Light Flash 10 Sec")
for i in range(0,5):
    time.sleep(1)
    lights(1)
    time.sleep(1)
    lights(0)
print("Status Light Test Done")
print("Input Test")
while True:
    #output=str(modeP.value())
    outputA ="Mode="+str(modeP.value())+"       Sensor="+str(senseP.value())+"         Man On="+str(manOnP.value())
    outputB="Man Off="+str(manOffP.value())+"    WIFI Enable="+str(wifiEnP.value())+"    Sensor Enable="+str(senseEnP.value())
    print(outputA)
    print(outputB)
    time.sleep_ms(1000)
