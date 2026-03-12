#espnow receiver
#esp_now_rx.py
#


#concept 1 - sleep 50ms on separate thread
#concept 2 - timer 50 ms with call back on separate thread
#concept 3 - timer 50 ms on main thread run.py

import network
import espnow
# from machine import Timer
# from time import sleep

import esp_parse_update

print('[esp_now_rx.py] - STARTED esp_now Wifi receiver')
# Initialize the Wi-Fi interface in station mode
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)


# Get the MAC address
mac = wifi.config('mac')

# Convert the MAC address to a human-readable format
mac_str = ':'.join('%02x' % b for b in mac)
print('MAC address:', mac_str)



#concept1
def espnow_receive(t):
# 
#     while True:

        peer, msg = e.recv(0)
        if msg:

            message = msg.decode('UTF-8').strip()
            print("[esp_now_rx.py] ", message)
            esp_parse_update.parse_and_update(message)
        





            
           


            
            





