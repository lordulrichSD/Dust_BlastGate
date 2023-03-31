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
    if wifiEnP():
        SetPlug('{"system":{"set_relay_state":{"state":0}}}')
        for x in range(0,20):   
            if getStatus():
                SetPlug('{"system":{"set_relay_state":{"state":0}}}')
                time.sleep_ms(10)
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
    
    s = socket.socket()
    s.settimeout(100)
    addr = socket.getaddrinfo(DCIP, 9999)[0][-1]
    encrypted = encrypt('{"system":{"get_sysinfo":{}}}')
    try:
        s.connect(addr)
        
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
