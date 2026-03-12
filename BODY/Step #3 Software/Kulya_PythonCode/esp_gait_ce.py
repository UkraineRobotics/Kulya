#this is gait - CE Collapse Expand
#it takes:
#   collection of legs

from math import sin, cos, radians, sqrt, atan2

import utime
from utime import sleep
import esp_context



def gait_ce(legs):
    
    group_blue = [legs[0], legs[2], legs[4]]
    group_green = [legs[1], legs[3], legs[5]]

    coxa_angle_limits = [0 , 0]
    femur_angle_limits = [94, 0]
    tibia_angle_limits = [-113, 0]
    
  
    
    ##receive gait from RC
   
#     print("[esp32_gait_walk.py] esp_context.RC_data[gait]: ", esp_context.RC_data["gait"])
 
    
    while esp_context.RC_data["gait"] == 'CE':   #until recieved new gait, keep doing current walk routine
      
      
        ce_value = int(esp_context.RC_data["ce_value"])
       
        def _map(x, in_min, in_max, out_min, out_max):              
            return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        
        
        for leg in legs:
            
            leg.current_angles=[0,
                                _map(ce_value, 0, 100, femur_angle_limits[0], femur_angle_limits[1]),
                                _map(ce_value, 0, 100, tibia_angle_limits[0], tibia_angle_limits[1])]
            leg.target_angles=leg.current_angles
            leg.past_angles=leg.current_angles
            
#             current_leg.coxa_angle = 0
#             current_leg.femur_angle = _map(ce_value, 0, 100, femur_angle_limits[0], femur_angle_limits[1])
#             current_leg.tibia_angle = _map(ce_value, 0, 100, tibia_angle_limits[0], tibia_angle_limits[1])
       
            
        ###Send command string to ch24
   
        
        
        ###Add time delay: do nothing if action time not elapsed sleep(0.9)
        
        
    
        
        
#     return gait