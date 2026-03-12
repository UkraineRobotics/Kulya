#this is gait - Roll - DOENST WORK - let us know if you create roll gait
#it takes:
#   collection of legs


import esp_context
from utime import sleep


def gait_roll(legs):
    

    coxa_angle_closed = 0
    femur_angle_closed = 94  #54
    tibia_angle_closed =-113  #-49
    
  
    
    ##receive gait from RC
    
    crnt = 0
    prev = 5
    
    while esp_context.RC_data["gait"] == 'ROLL':   #until recieved new gait, keep doing current walk routine
      
      
        roll_range = int(esp_context.RC_data["roll_range"])     #adjustment distance leg will open to have extra turn space, and/or upil downhill controll
        speed = 100 - int(esp_context.RC_data["speed"])
        roll_turn = int(esp_context.RC_data["roll_turn"])
      
        
        
        legs[crnt].target_angles = [coxa_angle_closed  - roll_turn/1.5,
                                       femur_angle_closed - roll_range + roll_turn,
                                       tibia_angle_closed + roll_range + roll_turn]
        
        legs[crnt].current_angles = legs[crnt].target_angles
        legs[crnt].past_angles = legs[crnt].target_angles
   
        if crnt == 0:  #replace with lengh legs
            prev = 5
        else:
            prev = crnt-1
        
        legs[prev].target_angles = [coxa_angle_closed, femur_angle_closed, tibia_angle_closed]
        legs[prev].current_angles = legs[prev].target_angles
        legs[prev].past_angles = legs[prev].target_angles
        
        crnt += 1
        
        if crnt > 5: #replace with lengh legs
            crnt = 0
            
        sleep(speed/1000)
        

        
        
        ###Add time delay: do nothing if action time not elapsed sleep(0.9)
        
        
    
        
        
#     return gait
