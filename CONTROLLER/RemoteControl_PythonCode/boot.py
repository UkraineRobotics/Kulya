# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import machine
from time import sleep



print('RC for KULYA')
print("ESP32 Started")



# giving a startup delay, so that the programmer can keyboard interrupt the lading and update firmaware
seconds_to_start = 2

print('starting in ',seconds_to_start) 
for i in range(seconds_to_start):
   print('.')
   sleep(1)
else:
    import sender   