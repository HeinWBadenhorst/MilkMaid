import neopixel
from machine import Pin, Timer
import time
import machine as mc
import math
from time import sleep
import initConfig
ws_pin = 0
led_num = 8

BRIGHTNESS = 1  # Adjust the brightness (1 - 25)
bay1Sol = Pin(14,Pin.OUT)    # GP14 is Output for Bay1 Solenoid (Pin-19)
bay2Sol = Pin(15,Pin.OUT)    # GP15 is Output for Bay2 Solenoid (Pin-20)
bay3Sol = Pin(16,Pin.OUT)    # GP16 is Output for Bay3 Solenoid (Pin-21)
bay4Sol = Pin(17,Pin.OUT)    # GP17 is Output for Bay4 Solenoid (Pin-22)
bay5Sol = Pin(18,Pin.OUT)    # GP18 is Output for Bay5 Solenoid (Pin-24)
bay6Sol = Pin(19,Pin.OUT)    # GP19 is Output for Bay6 Solenoid (Pin-25)
bay7Sol = Pin(20,Pin.OUT)    # GP20 is Output for Bay7 Solenoid (Pin-26)
bay8Sol = Pin(21,Pin.OUT)    # GP21 is Output for Bay8 Solenoid (Pin-27)
timer_bay1_count = 0
timer_bay2_count = 0
timer_bay3_count = 0
timer_bay4_count = 0
timer_bay5_count = 0
timer_bay6_count = 0
timer_bay7_count = 0
timer_bay8_count = 0
prgm_mode=False
neoRing = neopixel.NeoPixel(Pin(ws_pin), led_num)
next_button = Pin(11, Pin.IN)  # GP11 number pin is next button
select_button = Pin(12, Pin.IN)  # GP12 number pin is select button
end_button = Pin(13, Pin.IN)  # GP13 number pin is end button
position = 0  # Variable to keep track of the current position in the rainbow animation
brightness = .5  # Adjust the initial brightness (0.0 to 1.0)
mark_timer_bay1 = Timer(-1)
space_timer_bay1 = Timer(-1)
mark_timer_bay2 = Timer(-1)
space_timer_bay2 = Timer(-1)
mark_timer_bay3 = Timer(-1)
space_timer_bay3 = Timer(-1)
mark_timer_bay4 = Timer(-1)
space_timer_bay4 = Timer(-1)
mark_timer_bay5 = Timer(-1)
space_timer_bay5 = Timer(-1)
mark_timer_bay6 = Timer(-1)
space_timer_bay6 = Timer(-1)
mark_timer_bay7 = Timer(-1)
space_timer_bay7 = Timer(-1)
mark_timer_bay8 = Timer(-1)
space_timer_bay8 = Timer(-1)
selectButtonState = False
endButtonState = False
nextButtonState = False
currentBay = 1
vpmSelected = True

def convertToMSDelay(vpm_index):
    if vpm_index == 1:
        return 1200
    elif vpm_index == 2:
        return 1153 
    elif vpm_index == 3:
        return 1090 
    elif vpm_index == 4:
        return 1052 
    elif vpm_index == 5:
        return 1000 
    else:
        return 1000 

def convertToRestDelay(vpm_index,restIndex):
    if vpm_index == 1:
        if restIndex == 1:
            return 600
        elif restIndex == 2:
            return 720 
        elif restIndex == 3:
            return 840 
        else:
            return 600
    elif vpm_index == 2:
        if restIndex == 1:
            return 576
        elif restIndex == 2:
            return 691 
        elif restIndex == 3:
            return 807 
        else:
            return 600
    elif vpm_index == 3:
        if restIndex == 1:
            return 545
        elif restIndex == 2:
            return 654 
        elif restIndex == 3:
            return 763 
        else:
            return 600
    elif vpm_index == 4:
        if restIndex == 1:
            return 526
        elif restIndex == 2:
            return 632 
        elif restIndex == 3:
            return 732 
        else:
            return 600
    elif vpm_index == 5:
        if restIndex == 1:
            return 500
        elif restIndex == 2:
            return 600 
        elif restIndex == 3:
            return 700
        else:
            return 600
    else:
        if restIndex == 1:
            return 500
        elif restIndex == 2:
            return 600 
        elif restIndex == 3:
            return 700
        else:
            return 600

activeBay1 = initConfig.baySettings[0]["Active"]
activeBay2 = initConfig.baySettings[1]["Active"]
activeBay3 = initConfig.baySettings[2]["Active"]
activeBay4 = initConfig.baySettings[3]["Active"]
activeBay5 = initConfig.baySettings[4]["Active"]
activeBay6 = initConfig.baySettings[5]["Active"]
activeBay7 = initConfig.baySettings[6]["Active"]
activeBay8 = initConfig.baySettings[7]["Active"]
vpmIndexBay1 = initConfig.baySettings[0]["Settings"][0]
speedBay1 = convertToMSDelay(vpmIndexBay1)
vpmIndexBay2 = initConfig.baySettings[1]["Settings"][0]
speedBay2 = convertToMSDelay(vpmIndexBay2)
vpmIndexBay3 = initConfig.baySettings[2]["Settings"][0]
speedBay3 = convertToMSDelay(vpmIndexBay3)
vpmIndexBay4 = initConfig.baySettings[3]["Settings"][0]
speedBay4 = convertToMSDelay(vpmIndexBay4)
vpmIndexBay5 = initConfig.baySettings[4]["Settings"][0]
speedBay5 = convertToMSDelay(vpmIndexBay5)
vpmIndexBay6 = initConfig.baySettings[5]["Settings"][0]
speedBay6 = convertToMSDelay(vpmIndexBay6)
vpmIndexBay7 = initConfig.baySettings[6]["Settings"][0]
speedBay7 = convertToMSDelay(vpmIndexBay7)
vpmIndexBay8 = initConfig.baySettings[7]["Settings"][0]
speedBay8 = convertToMSDelay(vpmIndexBay8)
restIndexBay1 = initConfig.baySettings[0]["Settings"][1]
restIndexBay2 = initConfig.baySettings[1]["Settings"][1]
restIndexBay3 = initConfig.baySettings[2]["Settings"][1]
restIndexBay4 = initConfig.baySettings[3]["Settings"][1]
restIndexBay5 = initConfig.baySettings[4]["Settings"][1]
restIndexBay6 = initConfig.baySettings[5]["Settings"][1]
restIndexBay7 = initConfig.baySettings[6]["Settings"][1]
restIndexBay8 = initConfig.baySettings[7]["Settings"][1]
restBay1 = convertToRestDelay(vpmIndexBay1,restIndexBay1)
restBay2 = convertToRestDelay(vpmIndexBay2,restIndexBay2)
restBay3 = convertToRestDelay(vpmIndexBay3,restIndexBay3)
restBay4 = convertToRestDelay(vpmIndexBay4,restIndexBay4)
restBay5 = convertToRestDelay(vpmIndexBay5,restIndexBay5)
restBay6 = convertToRestDelay(vpmIndexBay6,restIndexBay6)
restBay7 = convertToRestDelay(vpmIndexBay7,restIndexBay7)
restBay8 = convertToRestDelay(vpmIndexBay8,restIndexBay8)

def getSpeedColor(vpmIndex):
    # Function to generate a color based on a position in the vpmIndex
    if vpmIndex == 0:
        return (10, 10, 0)  # Generate a grey color
    elif vpmIndex == 1:
        return (0, 10 * BRIGHTNESS, 0)  # Generate a green color
    elif vpmIndex == 2:
        return (0, 10 * BRIGHTNESS,  10 * BRIGHTNESS)  # Generate a cyan color
    elif vpmIndex == 3:
        return (0, 0, 10 * BRIGHTNESS)  # Generate a BLUE color
    elif vpmIndex == 4:
        return (10 * BRIGHTNESS, 0, 10 * BRIGHTNESS)  # Generate a MAGENTA color
    elif vpmIndex == 5:
        return (10 * BRIGHTNESS, 0, 0)  # Generate a RED color
    else:
        return (0, 0, 0)  # Generate a BLACK color

def getRestColor(restIndex):
    # Function to generate a color based on a position in the restIndex
    if restIndex == 1:
        return (0, 1, 0)  # Generate a green color
    elif restIndex == 2:
        return (0, 0, 1)  # Generate a blue color
    elif restIndex == 3:
        return (1, 0, 0)  # Generate a red color
    else:
        return (0, 0, 0)  # Generate a BLACK color

speedColorBay1 = getSpeedColor(vpmIndexBay1)
speedColorBay2 = getSpeedColor(vpmIndexBay2)
speedColorBay3 = getSpeedColor(vpmIndexBay3)
speedColorBay4 = getSpeedColor(vpmIndexBay4)
speedColorBay5 = getSpeedColor(vpmIndexBay5)
speedColorBay6 = getSpeedColor(vpmIndexBay6)
speedColorBay7 = getSpeedColor(vpmIndexBay7)
speedColorBay8 = getSpeedColor(vpmIndexBay8)
restColorBay1 = getRestColor(restIndexBay1)
restColorBay2 = getRestColor(restIndexBay2)
restColorBay3 = getRestColor(restIndexBay3)
restColorBay4 = getRestColor(restIndexBay4)
restColorBay5 = getRestColor(restIndexBay5)
restColorBay6 = getRestColor(restIndexBay6)
restColorBay7 = getRestColor(restIndexBay7)
restColorBay8 = getRestColor(restIndexBay8)

def int_handler_bay1_cb(timer):
    global neoRing,activeBay1,prgm_mode
    if prgm_mode == False:
        neoRing[0] = restColorBay1  # Set the color of the corresponding LED to restColorBay1
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay1Sol.value(0)

def int_handler_bay1(timer):
    global timer_bay1_count,neoRing,activeBay1,space_timer_bay1,prgm_mode
    if prgm_mode == False:
        timer_bay1_count += 1
        neoRing[0] = speedColorBay1  # Set the color of the corresponding LED to speedColorBay1
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay1Sol.value(1)
    space_timer_bay1 = Timer(period=restBay1, mode=Timer.ONE_SHOT, callback=int_handler_bay1_cb)

def int_handler_bay2_cb(pin):
    global neoRing,activeBay2,prgm_mode
    if prgm_mode == False:
        neoRing[1] = restColorBay2  # Set the color of the corresponding LED to restColorBay2
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay2Sol.value(0)

def int_handler_bay2(pin):
    global timer_bay2_count,neoRing,activeBay2,space_timer_bay2,prgm_mode
    if prgm_mode == False:
        timer_bay2_count += 1
        neoRing[1] = speedColorBay2  # Set the color of the corresponding LED to speedColorBay2
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay2Sol.value(1)
    space_timer_bay2 = Timer(period=restBay2, mode=Timer.ONE_SHOT, callback=int_handler_bay2_cb)

def int_handler_bay3_cb(pin):
    global neoRing,activeBay3,prgm_mode
    if prgm_mode == False:
        neoRing[2] = restColorBay3  # Set the color of the corresponding LED to restColorBay3
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay3Sol.value(0)

def int_handler_bay3(pin):
    global timer_bay3_count,neoRing,activeBay3,space_timer_bay3,prgm_mode
    if prgm_mode == False:
        timer_bay3_count += 1
        neoRing[2] = speedColorBay3  # Set the color of the corresponding LED to speedColorBay3
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay3Sol.value(1)
    space_timer_bay3 = Timer(period=restBay3, mode=Timer.ONE_SHOT, callback=int_handler_bay3_cb)

def int_handler_bay4_cb(pin):
    global neoRing,activeBay4,prgm_mode
    if prgm_mode == False:
        neoRing[3] = restColorBay4  # Set the color of the corresponding LED to restColorBay4
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay4Sol.value(0)

def int_handler_bay4(pin):
    global timer_bay4_count,neoRing,activeBay4,space_timer_bay4,prgm_mode
    if prgm_mode == False:
        timer_bay4_count += 1
        neoRing[3] = speedColorBay4  # Set the color of the corresponding LED to speedColorBay4
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay4Sol.value(1)
    space_timer_bay4 = Timer(period=restBay4, mode=Timer.ONE_SHOT, callback=int_handler_bay4_cb)

def int_handler_bay5_cb(pin):
    global neoRing,activeBay5,prgm_mode
    if prgm_mode == False:
        neoRing[4] = restColorBay5  # Set the color of the corresponding LED to restColorBay5
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay5Sol.value(0)

def int_handler_bay5(pin):
    global timer_bay5_count,neoRing,activeBay5,space_timer_bay5,prgm_mode
    if prgm_mode == False:
        timer_bay5_count += 1
        neoRing[4] = speedColorBay5  # Set the color of the corresponding LED to speedColorBay5
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay5Sol.value(1)
        space_timer_bay5 = Timer(period=restBay5, mode=Timer.ONE_SHOT, callback=int_handler_bay5_cb)

def int_handler_bay6_cb(pin):
    global neoRing,activeBay6,prgm_mode
    if prgm_mode == False:
        neoRing[5] = restColorBay6  # Set the color of the corresponding LED to restColorBay6
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay6Sol.value(0)

def int_handler_bay6(pin):
    global timer_bay6_count,neoRing,activeBay6,space_timer_bay6,prgm_mode
    if prgm_mode == False:
        timer_bay6_count += 1
        neoRing[5] = speedColorBay6  # Set the color of the corresponding LED to speedColorBay6
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay6Sol.value(1)
    space_timer_bay6 = Timer(period=restBay6, mode=Timer.ONE_SHOT, callback=int_handler_bay6_cb)

def int_handler_bay7_cb(pin):
    global neoRing,activeBay7,prgm_mode
    if prgm_mode == False:
        neoRing[6] = restColorBay7  # Set the color of the corresponding LED to restColorBay7
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay7Sol.value(0)

def int_handler_bay7(pin):
    global timer_bay7_count,neoRing,activeBay7,space_timer_bay7,prgm_mode
    if prgm_mode == False:
        timer_bay7_count += 1
        neoRing[6] = speedColorBay7  # Set the color of the corresponding LED to speedColorBay7
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay7Sol.value(1)
    space_timer_bay7 = Timer(period=restBay7, mode=Timer.ONE_SHOT, callback=int_handler_bay7_cb)

def int_handler_bay8_cb(pin):
    global neoRing,activeBay8,prgm_mode
    if prgm_mode == False:
        neoRing[7] = restColorBay8  # Set the color of the corresponding LED to restColorBay8
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay8Sol.value(0)

def int_handler_bay8(pin):
    global timer_bay8_count,neoRing,activeBay8,space_timer_bay8,prgm_mode
    if prgm_mode == False:
        timer_bay8_count += 1
        neoRing[7] = speedColorBay8  # Set the color of the corresponding LED to speedColorBay8
        neoRing.write()  # Update the WS2812 ring with the new colors
        bay8Sol.value(1)
        space_timer_bay8 = Timer(period=restBay8, mode=Timer.ONE_SHOT, callback=int_handler_bay8_cb)

def set_brightness(color):
    r, g, b = color
    r = int(r * BRIGHTNESS)
    g = int(g * BRIGHTNESS)
    b = int(b * BRIGHTNESS)
    return (r, g, b)

def wheel(pos):
    # Function to generate a color based on a position in the rainbow
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)  # Generate a red-yellow color
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)  # Generate a yellow-green color
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)  # Generate a green-blue color

def startUpLEDS():
    global position, brightness  # Use global variables for position and brightness

    for i in range(led_num):
        # Iterate through each LED in the ring
        hue = int(i * (255 / led_num) + position) % 256  # Calculate the hue value based on the LED position and current position
        color = wheel(hue)  # Get the color based on the calculated hue
        color = tuple(int(val * brightness) for val in color)  # Adjust the color brightness
        neoRing[(i + position) % led_num] = color  # Set the color of the corresponding LED
    neoRing.write()  # Update the WS2812 ring with the new colors
    position = (position + 1) % led_num  # Increment the position for the next iteration
    time.sleep_ms(50)  # Delay for a short period to control the animation speed

def clearLEDS():
    for i in range(led_num):
        # Iterate through each LED in the ring
        neoRing[i] = 0, 0, 0  # Set the color of the corresponding LED to black
    neoRing.write()  # Update the WS2812 ring with the new colors

def clearSols():
    global bay1Sol,bay2Sol,bay3Sol,bay4Sol,bay5Sol,bay6Sol,bay7Sol,bay8Sol
    bay1Sol.value(0)
    bay2Sol.value(0)
    bay3Sol.value(0)
    bay4Sol.value(0)
    bay5Sol.value(0)
    bay6Sol.value(0)
    bay7Sol.value(0)
    bay8Sol.value(0)

def displayCounts():
    global timer_bay1_count,timer_bay2_count,timer_bay3_count,timer_bay4_count,timer_bay5_count,timer_bay6_count,timer_bay7_count,timer_bay8_count
    print("Доильный зав 1 статистика =",timer_bay1_count,"засасывать")
    print("Доильный зав 2 статистика =",timer_bay2_count,"засасывать")
    print("Доильный зав 3 статистика =",timer_bay3_count,"засасывать")
    print("Доильный зав 4 статистика =",timer_bay4_count,"засасывать")
    print("Доильный зав 5 статистика =",timer_bay5_count,"засасывать")
    print("Доильный зав 6 статистика =",timer_bay6_count,"засасывать")
    print("Доильный зав 7 статистика =",timer_bay7_count,"засасывать")
    print("Доильный зав 8 статистика =",timer_bay8_count,"засасывать")
    print("***   Я бы хотел полететь на небо   ***")

def updateActiveJSONConfig(index,state):
    initConfig.baySettings[index]["Active"] = state
    initConfig.save_bay_data(initConfig.baySettings)

def updateSpeedJSONConfig():
    initConfig.baySettings[0]["Settings"][0] = vpmIndexBay1
    initConfig.baySettings[1]["Settings"][0] = vpmIndexBay2
    initConfig.baySettings[2]["Settings"][0] = vpmIndexBay3
    initConfig.baySettings[3]["Settings"][0] = vpmIndexBay4
    initConfig.baySettings[4]["Settings"][0] = vpmIndexBay5 
    initConfig.baySettings[5]["Settings"][0] = vpmIndexBay6
    initConfig.baySettings[6]["Settings"][0] = vpmIndexBay7
    initConfig.baySettings[7]["Settings"][0] = vpmIndexBay8
    initConfig.save_bay_data(initConfig.baySettings)

def updateRatioJSONConfig():
    initConfig.baySettings[0]["Settings"][1] = restIndexBay1
    initConfig.baySettings[1]["Settings"][1] = restIndexBay2
    initConfig.baySettings[2]["Settings"][1] = restIndexBay3
    initConfig.baySettings[3]["Settings"][1] = restIndexBay4
    initConfig.baySettings[4]["Settings"][1] = restIndexBay5 
    initConfig.baySettings[5]["Settings"][1] = restIndexBay6
    initConfig.baySettings[6]["Settings"][1] = restIndexBay7
    initConfig.baySettings[7]["Settings"][1] = restIndexBay8
    initConfig.save_bay_data(initConfig.baySettings)

def startTimers():
    global activeBay1,activeBay2,activeBay3,activeBay4,activeBay5,activeBay6,activeBay7,activeBay8,prgm_mode,mark_timer_bay1,mark_timer_bay2,mark_timer_bay3,mark_timer_bay4,mark_timer_bay5,mark_timer_bay6,mark_timer_bay7,mark_timer_bay8
    if activeBay1 == True:
        mark_timer_bay1 = Timer(period=speedBay1, mode=Timer.PERIODIC, callback=int_handler_bay1)
    if activeBay2 == True:
        mark_timer_bay2 = Timer(period=speedBay2, mode=Timer.PERIODIC, callback=int_handler_bay2)
    if activeBay3 == True:
        mark_timer_bay3 = Timer(period=speedBay3, mode=Timer.PERIODIC, callback=int_handler_bay3)
    if activeBay4 == True:
        mark_timer_bay4 = Timer(period=speedBay4, mode=Timer.PERIODIC, callback=int_handler_bay4)
    if activeBay5 == True:
        mark_timer_bay5 = Timer(period=speedBay5, mode=Timer.PERIODIC, callback=int_handler_bay5)
    if activeBay6 == True:
        mark_timer_bay6 = Timer(period=speedBay6, mode=Timer.PERIODIC, callback=int_handler_bay6)
    if activeBay7 == True:
        mark_timer_bay7 = Timer(period=speedBay7, mode=Timer.PERIODIC, callback=int_handler_bay7)
    if activeBay8 == True:
        mark_timer_bay8 = Timer(period=speedBay8, mode=Timer.PERIODIC, callback=int_handler_bay8)

startTimers()

for strt in range(20):
         startUpLEDS()
clearLEDS()

#Loop
while True:
    selectButtonState = select_button.value()
    endButtonState = end_button.value()
    nextButtonState = next_button.value()
    if endButtonState == True:
        if prgm_mode == True:
            vpmSelected = not vpmSelected
            print("Toggled")
            time.sleep(.8)
            endButtonState = end_button.value()
            if endButtonState == True:
                mc.reset()
    if selectButtonState == True:
        time.sleep(1)
        selectButtonState = select_button.value()
        if selectButtonState == True:
            clearLEDS()
            clearSols()
            prgm_mode=True
            currentBay = 1
            currentBayColor = getSpeedColor(vpmIndexBay1)  
            neoRing[0] = currentBayColor
            neoRing.write()  # Update the WS2812 ring with the new colors
            
    if prgm_mode == True:
        if vpmSelected == True:
            #print("Speed loop")
            nextButtonState = next_button.value()
            if nextButtonState == True:
                time.sleep(.8)
                nextButtonState = next_button.value()
                if nextButtonState == True:
#bay setting loop
                    clearLEDS()
                    currentBay += 1
                    if currentBay > 8:
                       currentBay = 1
                    print("currentBay")
                    print(currentBay)
                    if currentBay == 1:
                        currentBayColor = getSpeedColor(vpmIndexBay1)  
                        neoRing[0] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 2:
                        currentBayColor = getSpeedColor(vpmIndexBay2)  
                        neoRing[1] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 3:
                        currentBayColor = getSpeedColor(vpmIndexBay3)  
                        neoRing[2] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 4:
                        currentBayColor = getSpeedColor(vpmIndexBay4)  
                        neoRing[3] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 5:
                        currentBayColor = getSpeedColor(vpmIndexBay5)  
                        neoRing[4] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 6:
                        currentBayColor = getSpeedColor(vpmIndexBay6)  
                        neoRing[5] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 7:
                        currentBayColor = getSpeedColor(vpmIndexBay7)  
                        neoRing[6] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 8:
                        currentBayColor = getSpeedColor(vpmIndexBay8)  
                        neoRing[7] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                else:
 #colour setting loop                   
                    clearLEDS()
                    if currentBay == 1:
                        vpmIndexBay1 += 1
                        if vpmIndexBay1 > 5:
                           vpmIndexBay1 = 0
                           updateActiveJSONConfig(0,False)
                        else:
                           updateActiveJSONConfig(0,True)
                        updateSpeedJSONConfig()
                        currentBayColor = getSpeedColor(vpmIndexBay1)  
                        neoRing[0] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                        
                    elif currentBay == 2:
                        vpmIndexBay2 += 1
                        if vpmIndexBay2 > 5:
                           vpmIndexBay2 = 0 
                           updateActiveJSONConfig(1,False)
                        else:
                           updateActiveJSONConfig(1,True)
                        updateSpeedJSONConfig()
                        currentBayColor = getSpeedColor(vpmIndexBay2)  
                        neoRing[1] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 3:
                        vpmIndexBay3 += 1
                        if vpmIndexBay3 > 5:
                           vpmIndexBay3 = 0 
                           updateActiveJSONConfig(2,False)
                        else:
                           updateActiveJSONConfig(2,True)
                        updateSpeedJSONConfig()
                        currentBayColor = getSpeedColor(vpmIndexBay3)  
                        neoRing[2] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 4:
                        vpmIndexBay4 += 1
                        if vpmIndexBay4 > 5:
                           vpmIndexBay4 = 0 
                           updateActiveJSONConfig(3,False)
                        else:
                           updateActiveJSONConfig(3,True)
                        updateSpeedJSONConfig()
                        currentBayColor = getSpeedColor(vpmIndexBay4)  
                        neoRing[3] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 5:
                        vpmIndexBay5 += 1
                        if vpmIndexBay5 > 5:
                           vpmIndexBay5 = 0 
                           updateActiveJSONConfig(4,False)
                        else:
                           updateActiveJSONConfig(4,True)
                        updateSpeedJSONConfig()
                        currentBayColor = getSpeedColor(vpmIndexBay5)  
                        neoRing[4] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 6:
                        vpmIndexBay6 += 1
                        if vpmIndexBay6 > 5:
                           vpmIndexBay6 = 0 
                           updateActiveJSONConfig(5,False)
                        else:
                           updateActiveJSONConfig(5,True)
                        updateSpeedJSONConfig()
                        currentBayColor = getSpeedColor(vpmIndexBay6)  
                        neoRing[5] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 7:
                        vpmIndexBay7 += 1
                        if vpmIndexBay7 > 5:
                           vpmIndexBay7 = 0 
                           updateActiveJSONConfig(6,False)
                        else:
                           updateActiveJSONConfig(6,True)
                        updateSpeedJSONConfig()
                        currentBayColor = getSpeedColor(vpmIndexBay7)  
                        neoRing[6] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 8:
                        vpmIndexBay8 += 1
                        if vpmIndexBay8 > 5:
                           vpmIndexBay8 = 0 
                           updateActiveJSONConfig(7,False)
                        else:
                           updateActiveJSONConfig(7,True)
                        updateSpeedJSONConfig()
                        currentBayColor = getSpeedColor(vpmIndexBay8)  
                        neoRing[7] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
            #end next selected        
            else:
                clearLEDS()
                if currentBay == 1:
                    currentBayColor = getSpeedColor(vpmIndexBay1)  
                    neoRing[0] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 2:
                    currentBayColor = getSpeedColor(vpmIndexBay2)  
                    neoRing[1] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 3:
                    currentBayColor = getSpeedColor(vpmIndexBay3)  
                    neoRing[2] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 4:
                    currentBayColor = getSpeedColor(vpmIndexBay4)  
                    neoRing[3] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 5:
                    currentBayColor = getSpeedColor(vpmIndexBay5)  
                    neoRing[4] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 6:
                    currentBayColor = getSpeedColor(vpmIndexBay6)  
                    neoRing[5] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 7:
                    currentBayColor = getSpeedColor(vpmIndexBay7)  
                    neoRing[6] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 8:
                    currentBayColor = getSpeedColor(vpmIndexBay8)  
                    neoRing[7] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                time.sleep(.5)
        else:
            #Ratio loop
            nextButtonState = next_button.value()
            if nextButtonState == True:
                time.sleep(.8)
                nextButtonState = next_button.value()
                if nextButtonState == True:
                    clearLEDS()
                    currentBay += 1
                    if currentBay > 8:
                       currentBay = 1
                    print("currentBay ratio loop")
                    print(currentBay)
                    if currentBay == 1:
                        currentBayColor = getRestColor(restIndexBay1)  
                        neoRing[0] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 2:
                        currentBayColor = getRestColor(restIndexBay2)  
                        neoRing[1] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 3:
                        currentBayColor = getRestColor(restIndexBay3)  
                        neoRing[2] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 4:
                        currentBayColor = getRestColor(restIndexBay4)  
                        neoRing[3] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 5:
                        currentBayColor = getRestColor(restIndexBay5)  
                        neoRing[4] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 6:
                        currentBayColor = getRestColor(restIndexBay6)  
                        neoRing[5] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 7:
                        currentBayColor = getRestColor(restIndexBay7)  
                        neoRing[6] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 8:
                        currentBayColor = getRestColor(restIndexBay8)  
                        neoRing[7] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                else:
                    clearLEDS()
                    if currentBay == 1:
                        restIndexBay1 += 1
                        if restIndexBay1 > 3:
                           restIndexBay1 = 1
                        updateRatioJSONConfig()
                        currentBayColor = getRestColor(restIndexBay1)  
                        neoRing[0] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 2:
                        restIndexBay2 += 1
                        if restIndexBay2 > 3:
                           restIndexBay2 = 1 
                        updateRatioJSONConfig()
                        currentBayColor = getRestColor(restIndexBay2)  
                        neoRing[1] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 3:
                        restIndexBay3 += 1
                        if restIndexBay3 > 3:
                           restIndexBay3 = 1 
                        updateRatioJSONConfig()
                        currentBayColor = getRestColor(restIndexBay3)  
                        neoRing[2] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 4:
                        restIndexBay4 += 1
                        if restIndexBay4 > 3:
                           restIndexBay4 = 1 
                        updateRatioJSONConfig()
                        currentBayColor = getRestColor(restIndexBay4)  
                        neoRing[3] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 5:
                        restIndexBay5 += 1
                        if restIndexBay5 > 3:
                           restIndexBay5 = 1 
                        updateRatioJSONConfig()
                        currentBayColor = getRestColor(restIndexBay5)  
                        neoRing[4] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 6:
                        restIndexBay6 += 1
                        if restIndexBay6 > 3:
                           restIndexBay6 = 1 
                        updateRatioJSONConfig()
                        currentBayColor = getRestColor(restIndexBay6)  
                        neoRing[5] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 7:
                        restIndexBay7 += 1
                        if restIndexBay7 > 3:
                           restIndexBay7 = 1 
                        updateRatioJSONConfig()
                        currentBayColor = getRestColor(restIndexBay7)  
                        neoRing[6] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
                    elif currentBay == 8:
                        restIndexBay8 += 1
                        if restIndexBay8 > 3:
                           restIndexBay8 = 1 
                        updateRatioJSONConfig()
                        currentBayColor = getRestColor(restIndexBay8)  
                        neoRing[7] = currentBayColor
                        neoRing.write()  # Update the WS2812 ring with the new colors
            else:
                clearLEDS()
                if currentBay == 1:
                    currentBayColor = getRestColor(restIndexBay1)  
                    neoRing[0] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 2:
                    currentBayColor = getRestColor(restIndexBay2)  
                    neoRing[1] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 3:
                    currentBayColor = getRestColor(restIndexBay3)  
                    neoRing[2] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 4:
                    currentBayColor = getRestColor(restIndexBay4)  
                    neoRing[3] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 5:
                    currentBayColor = getRestColor(restIndexBay5)  
                    neoRing[4] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 6:
                    currentBayColor = getRestColor(restIndexBay6)  
                    neoRing[5] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 7:
                    currentBayColor = getRestColor(restIndexBay7)  
                    neoRing[6] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
                elif currentBay == 8:
                    currentBayColor = getRestColor(restIndexBay8)  
                    neoRing[7] = currentBayColor
                    neoRing.write()  # Update the WS2812 ring with the new colors
            #end next selected        
        #end vpm selected        
    #end program mode true
    else:
        time.sleep_ms(2000)  # Delay for a short period to control the stat print
        displayCounts()


