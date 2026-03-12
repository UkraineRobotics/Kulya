#esp_gait_selector
# this guy is called by run.py and runs in infinite loop
# it continiously look at esp_context[gait]
# and it loads up correesponding gait_%name%.py module

from utime import sleep
import esp_context

#importing known gaits
from esp_gait_walk import gait_walk
from esp_gait_ce import gait_ce
from esp_gait_leg import gait_leg
from esp_gait_roll import gait_roll
from esp_gait_wavr import gait_wavr
from esp_gait_wavl import gait_wavl
# from esp32_gait_roll import gait_roll

from esp_legs_setup import legs #mind just movin it from here in tho each patricular gait initialization. 

def gait_selector():
    print('gait_selector:   Started')
    while True:
           
        if esp_context.RC_data["gait"] == 'WALK':
            #>>HERE<< I can Optionally put transition into gait before the gait
            gait_walk(legs)
            
        elif esp_context.RC_data["gait"] == 'CE':
           
            gait_ce(legs)
        
        elif esp_context.RC_data["gait"] == 'LEG':
           
            gait_leg(legs)
        
        elif esp_context.RC_data["gait"] == 'ROLL':
            
            gait_roll(legs)

        elif esp_context.RC_data["gait"] == 'wavl':
            
            gait_wavl(legs)
            
        elif esp_context.RC_data["gait"] == 'wavr':
            
            gait_wavr(legs)
            
#         elif esp_context.RC_data["gait"] == 'STOP':
            #>>HERE<< I can Optionally put transition into Idle state
            # and make robot do somthing whil its idling by implementing idle gait
#             print("[esp32_gait_selector.py] gait STOP. IDLE")
        
        
        sleep(.5)    