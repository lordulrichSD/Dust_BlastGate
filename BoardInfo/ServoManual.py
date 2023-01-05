#manual servo postion test  Copy and paste to REPL
#then use servoSet(x) where x is a number between 0 and 100 to set position


import machine
import BoardInfo


def servoSet(pos):
    #sets servo, to value between 0 and 100
    posA = min(max(0, pos),100)
    outval=int(posA*.75)+40
    servo.duty(outval)
    #print(outval)
    
servoP=machine.Pin(BoardInfo.servoPin, machine.Pin.OUT)
servo = machine.PWM(servoP,freq=50)

