#esp_Leg_class.py

#this class is to create leg objects

#
# from math import sin, cos, radians, sqrt, atan2, acos, asin, pi, degrees


class Leg:


    def __init__(self,
                 leg_number,  # leg number 0..6 couterclockwise starting from right middle
                 pins):       #pins[coxa_pin, femur_pin, tibia_pin]: channels on ch24 servo controller
        
        #leg number and angle
        self.leg_number = leg_number
        
        leg_to_angle=[0,
                      60,
                      120,
                      180,
                      240,
                      300]
        
        self.leg_angle=leg_to_angle[self.leg_number]
        
        #setting up links length and joint offsets

        self.origin_distance = 41 #52 #a1
        self.coxa_length     = 10 #11      #a2
        self.femur_length    = 81 #95    #a3
        self.tibia_length    = 134 #162    #a4
        self.T2offset_angle  = 0  #90
        self.T3offset_angle  = -7 #13  #103    #T3offset 
        self.T4offset_angle  = 23  #208     #T4offset
        
        
        #connection to ch24servo controller
        self.pins = pins
        self.coxa_pin = pins[0]
        self.femur_pin = pins[1]
        self.tibia_pin = pins[2]
                
        #defining limit for angles
        self.coxa_limits = [-29,29]
        self.femur_limits = [-70,90]
        self.tibia_limits = [-90,36]
        
        #speed
        motor_max_speed = 0.67 #degrees/ms
        
        #calibration
        self.calibration = [0,  #coxa calibration, degrees
                            0,  #femur calibratiom, degrees
                            0]  #tibia calibration, degrees
        
     
        #selfknowledge: what are angles now 
        self.past_angles = [0,0,0] 
        self.current_angles = [0,0,0]    # (coxa_angle, femur_angle, tibia_agnle)   #the list with current angles
        self.target_angles = [0,0,0]  # the tagret where to reach to smoothly
        self.on_target = False
        


        

    def is_on_target(self):
        self.on_target = (self.target_angles == self.current_angles)
        if self.on_target:
            self.past_angles = self.target_angles
            
        return self.on_target
    
    
    
#     def set_current_angles(self, _current_angles):
#         self.current_angles = _current_angles
#         
#         self.is_on_target
#             
#     def set_target_angles(self, _target_angles):
#         self.target_angles = _target_angles
#         
#         self.is_on_target
# 
#     def set_past_angles(self, _past_angles):
#         self.past_angles = _past_angles
#         
#         self.is_on_target
#         
 
 