#esp_context.py
#this module create an array for storing parsed data between modules

RC_data = {"gait":'STOP',
           "spread": 115, #105
           "height": 120, #95
           "raise":55,
           "turn_angle":0, #turn_angle
           "speed":0, #0..100%
           "dx":0, #dx
           "dy":0, #dy
           "rx":0,      #base rotation
           "ry":0,
           "espi":90,    #ms
           "servoi":150,  #ms
           "rz":0,
           "ce_value":100,
           "leg_num":0,
           "coxa":0,
           "femur":0,
           "tibia":0,
           "J_mode":'steer',
           "J_x"   :0,
           "J_y"   :0
#            "roll_range":10,
#            "roll_turn":0
           }

# Joystick_data = {"J_mode":'sides',
#                  "J_x"   :0,
#                  "J_y"   :0
#                  }

last_comandStr = ''



legmover_on = False
in_transition = False

motor_max_speed = 100/0.9 #60 degres per 0.9 sec

motion_smooth_rate = .2

# esp_interval = 0.001
# servo_interval = 0.005