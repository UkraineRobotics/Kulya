#esp_inverse_kinematics.py

#tis a separate inverse kinematiks module

from math import sin, cos, radians, sqrt, atan2, acos, asin, pi, degrees

def IK(leg, xyz):
    try:
            
        x,y,z = xyz
        
        #zero division avoidance
        if x==0: x+=0.0000001
        if y==0: x+=0.0000001
        if z==0: x+=0.0000001
        
        #'matching angles
        T1 = leg.leg_angle #theta1 angle
        T1 = radians(T1)  #making radians from degrees
        
        #matching links lentgh
        # origin_distance, coxa_length, femur_length, tibia_length, T3offset_angle, T4offset_angle
        # we take characteristict from a particular leg. so theoretically each leg can be defferent configuration
        
        a1 = leg.origin_distance
        a2 = leg.coxa_length
        a3 = leg.femur_length
        a4 = leg.tibia_length


        #Inverse Kinematics
        #-leg top view
    # 
    #                 
    #    y            [x,y,z]   
    #                 /a4                  	     T1 : leg angle
    #           (T4)./                     	     a1 : distance from robot origing to leg origin
    #               /a3                    	     a2 : coxe lenght
    #         (T3)./                       	     a3 : femur lenght
    #             /                        	     a4 : tibia lenght
    #    T1      / a2                      	 [x,y,z]: endeffector
    #    ._____./ T2     x
    #    o 	 a1


        x1_0 = a1*cos(T1) #leg origin X
        y1_0 = a1*sin(T1) #leg origin Y

        
        #check if input coordinates x and y are phisically reachable
    #     if((x**2+y**2)>(a1+a2+a3+a4)**2):      #if x,y are further away than fully streched leg
    #         x = .7* (a1+a2+a3+a4) * cos(T1)    #reduce x,y to
    #         y = .7* (a1+a2+a3+a4) * sin(T1)    #.7 of max strech
    #         # tododo here i want to raise a flag of x,y limit reached
        
        b = sqrt((x - x1_0)**2+(y - y1_0)**2)                               #(0)  hypotenuse on top view   
        T2 = T1 - atan2((y-y1_0),(x-x1_0))     #asin((y - y1_0)/b)-T1       #(1) T2 = coxa angle radians


        #-leg side view
    #             
    #                       .T4                	       c : side   T3 -- [xyz]
    #                      /\                  	       d : side   T1 -- [xyz]
    #                  a3 /  \                 	   alpha : angle  a2 \/ c
    #                    /    \                	   beta  : angle  c  \/ a3
    #     (T1) (T2)  T3 /      \               	   gamma : angle  a3 \/ a4
    #      ._ _ _.____./        \ a4
    #         a1   a2            \
    #                             \[x,y,z]
    # 


        if b == a2:
            b+=0.0000001 # ensuring c-2 and a-2c is never 0 (zero division avoidance)
        
        c = sqrt( z**2 + (b-a2)**2 )  #(1)
        d = sqrt( z**2 + b**2)
        
        if c == 0:
            c+=0.0000001 #(zero division avoidance)
        
        ##??? c < a3+a4 
        
        if d == 0:
            d+=0.0000001
        ## tododod d is the distance between robot origin and end-effector. im must be more than base radius
        # maybe add if d< a1: d = a1       
        
        
        
        
        alpha = acos( (a2**2 + c**2 - d**2) / (2*a2*c) )
        beta = acos( (a3**2+ c**2 - a4**2) / (2*a3*c) )
        gamma = acos( (a3**2+ a4**2 - c**2) / (2*a3*a4))
            
    #         T3 = (alpha + beta) - pi 
    #         T4 = -(gamma- pi)
        T3 = beta - (pi - alpha)
        T4 = -(pi/2 - gamma)
    #     T4 = gamma - pi
         

     
        #making degrees from radians
        T2 = degrees(T2)
        T3 = degrees(T3)
        T4 = degrees(T4)
        
        if T2 > 180:        #this section needed to make sure all angles between 0-1800 degrees
            T2 -= 360       #without it coxas on the one half of the robot won't function
        if T3 > 180:        # because for them angles gona calculate as between 180 and 360
            T3 -= 360
        if T4 > 180:
            T4 -= 360
        
        if T2 < -180:
            T2 += 360
        if T3 < -180:
            T3 += 360
        if T4 < -180:
            T4 += 360

        

        coxa_angle = round(T2)
        femur_angle = round(T3)
        tibia_angle = round(T4)
        
        #control limits
        if coxa_angle < leg.coxa_limits[0]:
            coxa_angle = leg.coxa_limits[0]
        elif coxa_angle > leg.coxa_limits[1]:
            coxa_angle = leg.coxa_limits[1]
        
        if femur_angle < leg.femur_limits[0]:
            femur_angle = leg.femur_limits[0]
        elif femur_angle > leg.femur_limits[1]:
            femur_angle = leg.femur_limits[1]
        
        if tibia_angle < leg.tibia_limits[0]:
            tibia_angle = leg.tibia_limits[0]
        elif tibia_angle > leg.tibia_limits[1]:
            tibia_angle = leg.tibia_limits[1]
        
        
        
#         print('[Leg_class.py] INV_KCS  got coordinates: ', x, y, z, '    return angles: ', coxa_angle, femur_angle, tibia_angle)
        
        return([coxa_angle, femur_angle, tibia_angle])
        
    except Exception as e:
       #print type of error occurring
        print("Inverse Kinematics Error: ",e)
        return(leg.current_angles)





#calculates leg spread reference point
def getSpread_xyz(leg, spread_radius_, turn_angle_, height_, dx_, dy_, rx_, ry_, rz_):
    

    
    x = (spread_radius_*cos(radians(leg.leg_angle+turn_angle_+rz_))+dx_) 
    y = (spread_radius_*sin(radians(leg.leg_angle+turn_angle_+rz_))+dy_)   
    z = ry_*spread_radius_*sin(radians(leg.leg_angle+turn_angle_))+rx_*spread_radius_*cos(radians(leg.leg_angle+turn_angle_))-1-height_


    return [x,y,z]
