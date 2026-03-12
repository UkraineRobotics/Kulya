#run.py
#this file is launching everything
#And it gives a bit of start up delay
#so you can interrupt and update firmavare 


from time import sleep

import esp_context   #this structure contains data that Kulya recevied from RC
import esp_legs_setup #this file initializes the each leg individually and creates collection legs

#startin Bluetooth Low Enegry (BLE)
# this thing connects Kylya with mobile phone Remote Control (RC) app
from esp_ble import ESP32_BLE
ESP32_BLE("KULYA v4 OpenSource DIY")     #ble process is trigerred by timer interupt. it resides on system Timer1

# and that thing connects Kylya with physical RC
from esp_now_rx import espnow_receive
from machine import Timer
tim = Timer(-1)
tim.init(period=50, mode=Timer.PERIODIC, callback=espnow_receive)


import _thread

from esp_legmover import legmover
_thread.start_new_thread(legmover,())  #starting legmover on separate thread


#once context is created and legs are set up
#robot can launch Gait_selector

sleep(.100)
esp_context.legmover_on= True
print("esp_context.legmover_on")

from esp_gait_selector import gait_selector
gait_selector()  #it checks data in context and launches corresponding gait file










