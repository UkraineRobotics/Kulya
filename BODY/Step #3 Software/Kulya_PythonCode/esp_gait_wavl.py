#this is gait - wavl - wave left leg
#it takes:
#   collection of legs


import esp_context
from esp_legs_setup import legs

from time import sleep
from esp_inverse_kinematics import IK,getSpread_xyz
from math import radians



esp_context.motion_smooth_rate = .25
        
spread_radius = 115
height = 120
shift_dx = 0
shift_dy = -20
rx = 0
ry = radians(8)
rz = 0


frame = 0

frames = [0,1,2,3,4,5,6]

legs_on_target = False
    
             
    
def move_to_frame(frame):
            
            
    if frame == 0:   #shift body backward
        print('!!!!FRAME 0 ')
        esp_context.motion_smooth_rate = .35
        
    if frame == 1:
        for leg in legs:
            leg.target_angles = IK(leg, getSpread_xyz(leg,
                                                      spread_radius,
                                                      0,
                                                      height,
                                                      shift_dx,
                                                      shift_dy,
                                                      rx,
                                                      ry,
                                                      rz))
        legs[4].target_angles = [0,60,8]

                 
    if frame == 2:
        esp_context.motion_smooth_rate = .0001
        legs[4].target_angles = [-20,60,8]
         
    if frame == 3:
        legs[4].target_angles = [20,60,8] 
         
    if frame == 4:
        legs[4].target_angles = [-20,60,8]           
        
    if frame == 5:
        legs[4].target_angles = [20,60,8]             
    
    if frame == 6:
        esp_context.motion_smooth_rate = .7
        for leg in legs:
            
            leg.target_angles = IK(leg, getSpread_xyz(leg, spread_radius, 0, height, 0, 0, rx, ry, rz))
        
        esp_context.RC_data["gait"] ='WALK'  #quit waiving gate
        
                


def gait_wavl(legs):
    global frame, frames
    frame = 0
        
    print("gait:wavl - wave left leg")



    while esp_context.RC_data["gait"] == 'wavl':   #until recieved new gait, keep doing current walk routine


        
        
        
        
            
        #MOVING LEGS TO NEXT FRAME,
      
        #checking if legs reached their destination
        legs_on_target = True
        
        for leg in legs:
        
            legs_on_target = legs_on_target and leg.is_on_target()

        #IF LEGS ARE on target position WE GOTTA UPDATE FRAME
        if legs_on_target:
            print('frame ', frame)
            frame += 1 #itr #moving to next frame
        if frame > len(frames)-1:
            frame = 0
            
        
    
        


        move_to_frame(frames[frame])
        
        

        
        

       
