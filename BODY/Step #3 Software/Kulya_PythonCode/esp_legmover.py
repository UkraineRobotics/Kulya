## this is a leg mover
# it takes a collection of legs as a 1st argument
# and time to complete the action as a 2nd argument
# all legs in collection group will arrive to their targets simultaneousely

#angles are set by .inverse_kcs for a given leg, or by leg(self).coxa/femur/tibia_angle

import machine
from time import time, sleep
#UART
uart = machine.UART(2, 9600)


import esp_context
from esp_legs_setup import legs

esp_interval = 0.100
servo_interval = 0.120

esp_context.motion_smooth_rate = .2 #the higher the number the slower it smoothes 

def deg2pulse(x):       #, in_min, in_max, out_min, out_max):
    in_min = -90    
    in_max = 90
    out_min = 500
    out_max = 2500
    
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def speed2steps(x):       #, in_min, in_max, out_min, out_max):
    in_min = 1    
    in_max = 100
    out_min = 10
    out_max = 1
    
    return ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def legmover():
    print("LegMover STARTED")
    
    current_speed = 0
    substep = 0
    
    while True:
        if (esp_context.legmover_on):           
            
            esp_interval = int(esp_context.RC_data["espi"]) /1000
            servo_interval = int(esp_context.RC_data["servoi"]) /1000
            
            
#             s = 0.15 #smoothing rate
#             current_speed = ( int(esp_context.RC_data["speed"])*s) + (current_speed*(1-s) )


            current_speed =  int(esp_context.RC_data["speed"])
            
            comandStr = '' #string for command to sent to ch24
            
    
        
        
        
            if (current_speed >= 1):
                
                substeps_number = speed2steps(current_speed)
                substep_next=1
             
                for leg in legs:
                    for i in range(3):
                        leg.current_angles[i] = leg.past_angles[i] + substep*(leg.target_angles[i]-leg.past_angles[i])/substeps_number
            
                substep += substep_next
                
                if (substep >= substeps_number):
                    for leg in legs:
                        leg.current_angles = leg.target_angles
                    substep = 1  # NEED TO CHECK POSSIBLY 0
                    
            elif (current_speed==0):
#                 for leg in legs:
#                     leg.current_angles = leg.target_angles
                     
                for leg in legs:
                    for i in range(3): #low pass filter for smoothing leg movement
                        leg.current_angles[i] = leg.target_angles[i]*(1-esp_context.motion_smooth_rate) + leg.current_angles[i]*esp_context.motion_smooth_rate              
                        
                        if ( abs( leg.target_angles[i]-leg.current_angles[i] ) < .5 ):
                             leg.current_angles[i] = leg.target_angles[i]
   
            
            
            
            for leg in legs:
                comandStr += '#'+str(leg.pins[0])  
                comandStr += 'P'+str(3000-deg2pulse(leg.current_angles[0] +   leg.calibration[0] + leg.T2offset_angle))   
                comandStr += '#'+str(leg.pins[1])  
                comandStr += 'P'+str(deg2pulse(leg.current_angles[1]      +   leg.calibration[1] + leg.T3offset_angle))    
                comandStr += '#'+str(leg.pins[2])  
                comandStr += 'P'+str(3000-deg2pulse(leg.current_angles[2] +   leg.calibration[2] + leg.T4offset_angle))    

            comandStr += 'T' + str(round(servo_interval*1000))
            
#             
            uart.write(comandStr +'\r\n')
#             r=uart.read()       
                
                
                
                
            sleep(esp_interval)
                
                
                
      

            ###CHEKING LEG LIMITS
                    #control limits
#             for leg in legs:
#                 if leg.target_angles[0] < leg.coxa_limits[0]:
#                     leg.target_angles[0] = leg.coxa_limits[0]
#                 elif leg.target_angles[0] > leg.coxa_limits[1]:
#                     leg.target_angles[0] = leg.coxa_limits[1]
#                 
#                 if leg.target_angles[1] < leg.femur_limits[0]:
#                     leg.target_angles[1] = leg.femur_limits[0]
#                 elif leg.target_angles[1] > leg.femur_limits[1]:
#                     leg.target_angles[1] = leg.femur_limits[1]
#                 
#                 if leg.target_angles[2] < leg.tibia_limits[0]:
#                     leg.target_angles[2] = leg.tibia_limits[0]
#                 elif leg.target_angles[2] > leg.tibia_limits[1]:
#                     leg.target_angles[2] = leg.tibia_limits[1]
            
            
            
  