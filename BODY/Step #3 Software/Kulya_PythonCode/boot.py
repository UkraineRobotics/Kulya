# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import machine
from utime import sleep


# Connecting "libs" folder
# import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, '/libs')


print('KULYA')
print("ESP32 Started")



# giving a startup delay, so that the programmer can keyboard interrupt the lading and update firmaware
seconds_to_start = 3

print('starting in ',seconds_to_start) 
for i in range(seconds_to_start):
   print('.')
   sleep(1)
else:
    import run   #launcing Run file. the one that start all other components