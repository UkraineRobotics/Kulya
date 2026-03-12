#this is gait - leg
#it takes:
#   collection of legs


import esp_context
from time import sleep


def gait_leg(legs):
    
    group_blue = [legs[0], legs[2], legs[4]]
    group_green = [legs[1], legs[3], legs[5]]

    coxa_angle_limits = [0 , 0]
    femur_angle_limits = [74, 0]
    tibia_angle_limits = [-69, 0]
    
    esp_context.motion_smooth_rate = .4
    
    ##receive gait from RC
   
#     print("[esp32_gait_walk.py] esp32_RC_data.RC_data[gait]: ", esp32_RC_data.RC_data["gait"])
 
    
    while esp_context.RC_data["gait"] == 'LEG':   #until recieved new gait, keep doing current walk routine
      
      
        leg_num = int(esp_context.RC_data["leg_num"])
        coxa = int(esp_context.RC_data["coxa"])
        femur = int(esp_context.RC_data["femur"])
        tibia = int(esp_context.RC_data["tibia"])
        
        
                
        legs[leg_num].target_angles = [coxa, femur, tibia]
#         legs[leg_num].current_angles = legs[leg_num].target_angles
#         legs[leg_num].past_angles = legs[leg_num].target_angles
        
        if (legs[leg_num].target_angles == legs[leg_num].current_angles): #leg on target
            legs[leg_num].past_angles = legs[leg_num].target_angles
        
        #sleep(.200)
        
       