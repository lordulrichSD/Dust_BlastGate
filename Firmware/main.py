#main file for Blast Gate





    
#Sense operating position
if manOnP.value():
    #Manual On
    print("Manual On")
    #if on==False:
    TurnOnDC()          
    on = True

elif manOffP.value():
    print("Manual Off")
    time.sleep(delayTime)
    if on==True:
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
        senseStatusP.value(1)
        time.sleep(delayTime)
        if on==True:
            TurnOffDC()
        on = False           
else :
    on = False

