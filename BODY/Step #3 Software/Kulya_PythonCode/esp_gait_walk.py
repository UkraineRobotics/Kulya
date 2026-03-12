#this is gait - WALK
#it takes:


from math import sin, cos, radians, sqrt, atan2, pi
from esp_legmover import legmover
import time

from machine import I2C, Pin
# import mpu6050
# i2c = I2C(scl=Pin(22), sda=Pin(21))
# accelerometer = mpu6050.accel(i2c)
# accelerometer.get_values()




import esp_context
# from esp_legs_setup import legs

from esp_inverse_kinematics import IK, getSpread_xyz



turn_angle  = int(esp_context.RC_data["turn_angle"])  
speed       = int(esp_context.RC_data["speed"]) 
dx          = int(esp_context.RC_data["dx"])  
dy          = int(esp_context.RC_data["dy"])  
spread_radius = int(esp_context.RC_data["spread"])
height      = int(esp_context.RC_data["height"])
raise_h     = int(esp_context.RC_data["raise"])
rx = int(esp_context.RC_data["rx"])/100  
ry = int(esp_context.RC_data["ry"])/100  
rz = int(esp_context.RC_data["rz"]) 

shift_dx = 0
shift_dy = 0


#gyroscope data 
alpha = 0.08  # Replace with the actual value
beta = 0.02 
pitch = 0
roll = 0




def gait_walk(legs):

    
    i = 0 # iterator. +1 fo forward  0 for stop (not implemented -1 for backward)
    frame = 1
    
              #0,1,2,3#
    frames = [[1,2,3,4],
              [3,4,1,2]]
    
    group_blue = [legs[0], legs[2], legs[4]]
    group_green = [legs[1], legs[3], legs[5]]
    
    legs_on_target = False
    
    current_time = time.ticks_ms()
    last_time = current_time
    dt = (current_time - last_time) / 1000.0
    
    esp_context.motion_smooth_rate = .25




    
    
    
    
    def move_to_frame(leg, frame):
        

#         -----(2)
#         -----/\
#         ----/--\
#         ---/----\
#         --/------\
#         -/________\
#         (1)--(4)--(3)
    
        xyz1 = getSpread_xyz(leg, spread_radius, -turn_angle, height, -dx, -dy, rx, ry, rz) # 0, 0)
        
        xyz2 = getSpread_xyz(leg, spread_radius, 0, height-raise_h, shift_dx, shift_dy, rx, ry, rz)
        
        xyz3 = getSpread_xyz(leg, spread_radius, turn_angle, height, dx, dy, rx, ry, rz)    #front point  - reach to (3)
        
        xyz4 = getSpread_xyz(leg, spread_radius, 0, height, shift_dx, shift_dy, rx, ry, rz)
        
        if frame == 1:
            leg.target_angles = IK(leg, xyz1) 
                     
        if frame == 2:
            leg.target_angles = IK(leg, xyz2) 
             
        if frame == 3:
            leg.target_angles = IK(leg, xyz3) 
             
        if frame == 4:
            leg.target_angles = IK(leg, xyz4) 


    while esp_context.RC_data["gait"] == 'WALK':   #until recieved new gait, kepp doing current walk routine
        
        
      
        turn_angle  = int(esp_context.RC_data["turn_angle"])  
        speed       = int(esp_context.RC_data["speed"]) 
        dx          = int(esp_context.RC_data["dx"])  
        dy          = int(esp_context.RC_data["dy"])  
        spread_radius = int(esp_context.RC_data["spread"])
        height      = int(esp_context.RC_data["height"])
        raise_h     = int(esp_context.RC_data["raise"])
        rx = int(esp_context.RC_data["rx"])/100  
        ry = int(esp_context.RC_data["ry"])/100  
        rz = int(esp_context.RC_data["rz"])
        shift_dx = 0
        shift_dy = 0

        
        
        
        if (speed <= 0) & (frame == 0 | frame == 2):     # ground all legs ang move within frame 4
            speed = 25

                
        if (speed <= 0) & (frame == 1 | frame == 3):     # ground all legs ang move within frame 4
            raise_h = 0
            shift_dx = -dx
            shift_dy = -dy
            

            
        else: #MOVING LEGS TO NEXT FRAME,
            raise_h = int(esp_context.RC_data["raise"])
            shift_dx = 0
            shift_dy = 0
            
            #checking if legs reached their destination
            legs_on_target = True
            
            for leg in legs:
 
 
                legs_on_target = legs_on_target and leg.is_on_target()
    
            #IF LEGS ARE on target position WE GOTTA UPDATE FRAME
            if legs_on_target:          
                frame += 1 #itr #moving to next frame
            if frame > 3:
                frame = 0               
                
                
        #green group go frames 1234
        for leg in group_green:
            move_to_frame(leg, frames[0][frame])
            
        #blue group go frames 3412
        for leg in group_blue:
            move_to_frame(leg, frames[1][frame])                 
         




   
        

        
    