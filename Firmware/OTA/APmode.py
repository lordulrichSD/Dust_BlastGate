#Code to run in Access Point Mode- i.e. when updating settings

#create webpage for updating settings

codeVersion="1.0"

def webpage(SSID, Password, DCIP, Closed, Open, Delay):

    #build webpage HTML
    htmll=[]
    htmll.append('''<!DOCTYPE html>
    <html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <body> 

    <h1>Blast Gate Settings</h1>
    <form enctype="text/plain" method="post">
    <input type="hidden" id="formstart" name="formstart" value="starthere">
    <label for SSID="SSID">SSID: </label>
    <input type="text" id="SSID" name="SSID" value="''')
    
    htmll.append(str(SSID))
    htmll.append('''"><br>
    <label for Password="Password">Password: </label>
    <input type="password" id="Password" name="Password" value="''')
    htmll.append(str(Password))
    htmll.append(''' "><br>
    <label for DCIP="DCIP">Dust Collector IP Address:  </label>
    <input type="text" id="DCIP" name="DCIP" value="''')
    htmll.append(str(DCIP))
    htmll.append('''"><br>
    <label for Closed="Closed">Closed Position: </label>
    <input type="number" id="Closed" name="Closed" min="0" max="100" value="''')
    htmll.append(str(Closed))
    htmll.append('''"><br>
    <label for Open="Open">Open Position: </label>
    <input type="number" id="Open" name="Open" min="0" max="100"value="''')
    htmll.append(str(Open))
    htmll.append('''"><br>
    <label for Delay="Delay">Delay Time (Sec): </label>
    <input type="number" id="Delay" name="Delay" min="0" max="120"value="''')
    htmll.append(str(Delay))
    htmll.append('''"><br>
    <label for Delay2="Delay2">Delay2 Time (Sec): </label>
    <input type="number" id="Delay2" name="Delay2" min="0" max="30"value="''')
    htmll.append(str(Delay2))
    htmll.append('''"><br>
    <label for Update="Update">Check for and Download Update :</label>
    <input type="radio" id="Update" name="Update" value="1"><br>
    <label for="dont">Don't Update</label>
    <input type="radio" id="dont" name="Update" value="0"><br>
    <input type="submit" value="Submit">
    <input type="hidden" id="formend" name="formend" value="endhere">
    </form><br>
    Firmware Version ''')
    htmll.append(codeVersion)
    htmll.append('''</body>
    </html>''')
    html=''.join(htmll)
#     print(html)
    return html

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


def savesettings(SSID, password, DCIP, closedPos, openPos, delayTime):
    f=open("Settings.py", "w")
    f.write("#configuration settings - i.e. wifi Deployed Device Specific\n")

    f.write("SSID='")
    f.write(str(SSID))
    f.write("'\n")
    
    f.write("password='")
    f.write(str(password))
    f.write("'\n")
    
    f.write("DCIP='")
    f.write(str(DCIP))
    f.write("'\n")

    f.write("closedPos=")
    f.write(str(closedPos))
    f.write("\n")
    
    f.write("openPos=")
    f.write(str(openPos))
    f.write("\n")
    
    f.write("delayTime=")
    f.write(str(delayTime))
    f.write("\n")
    
    f.write("delay2=")
    f.write(str(delay2))
    f.write("\n")
    f.close()

def run():

    #get current settings()
    import Settings
    SSID = Settings.SSID
    password = Settings.password
    DCIP= Settings.DCIP
    closedPos=Settings.closedPos
    openPos= Settings.openPos
    delayTime=Settings.delayTime

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
    
    waiting=True
    while (waiting):
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        strrequest=str(request)
        print(strrequest)
        ispost=strrequest.startswith("b'POST")
        print(ispost)
        if (ispost):
            print("process POST request")
            postStart=strrequest.find("formstart=starthere")
            print(postStart)
            trimpoint=postStart+23
            postdata=strrequest[trimpoint:]
#             print("POST info")
#             print(postdata)
            list1=postdata.split('\\r\\n')
#             print(list1)
            list2=[]
            for i in list1 :
                row=i.split("=")
#                 print("Row")
#                 print(row)
                list2.append(row)
            print("Final List")
            print(list2) 
            for i in list2:
                var=i[0]
                if var=="SSID":
                    SSID=i[1]
                elif var=="Password":
                    password=i[1]
                elif var=="DCIP":
                    DCIP=i[1]
                elif var=="Closed":
                    closedPos=int(i[1])
                elif var=="Open":
                    openPos=int(i[1])
                elif var=="Delay":
                    delayTime=int(i[1])
                elif var=="Delay2":
                    delayTime=int(i[1])
                elif var=="Update":
                    if i[1]=="1":
                        update=True
                
            savesettings(SSID, password, DCIP, closedPos, openPos, delayTime)
                
            if update:
                print("Checking for Update")
                ap.active(False)
                connectWIFI()
                                      
        
        html = webpage(SSID, password, DCIP, closedPos, openPos, delayTime)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(html)
        conn.close()
    

