#esp32_legs_setup.py
# this is legs initialization and
# initial calibration
# runs Once in module boot.py

from utime import sleep
from esp_Leg_class import Leg

#create 6 legs

leg0 = Leg(0, [1 , 2 , 3])  #right front
leg1 = Leg(1, [6 , 7 , 8])  #left front
leg2 = Leg(2, [9 , 10, 11] )  #left mid
leg3 = Leg(3, [14, 15, 16] )  #left rear..........
leg4 = Leg(4, [17, 18, 19] )  #right rear........
leg5 = Leg(5, [22, 23, 24] )  #right mid...............


       

#calibration
leg0.calibration=[3,9,7]
leg1.calibration=[-5,7,3]
leg2.calibration=[-8,3,0]
leg3.calibration=[-7,16,16]
leg4.calibration=[-14,-10,6]
leg5.calibration=[-3,10,2]


# leg0.calibration=[0, 0, 0]
# leg1.calibration=[0, 0, 0]
# leg2.calibration=[0, 0, 0]
# leg3.calibration=[0, 0, 0]
# leg4.calibration=[0, 0, 0]
# leg5.calibration=[0, 0, 0]

# creating Global collection of legs
legs = [leg0, leg1, leg2, leg3, leg4, leg5]  


    
