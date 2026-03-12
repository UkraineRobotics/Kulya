#run.py
#this file is launching everything


import network
import esp
import espnow
from machine import Pin, ADC, Timer
import time
from time import sleep
from math import sqrt

# Initialize the Wi-Fi interface in station mode
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

interval = .050
# Debounce time in milliseconds
debounce_time = 200

# Last time the button was pressed
last_press_time = 0



peers = [
#     YOU MUST ENTER YOUR KULYA MAC HERE
    b'\xAA\xAA\xAA\xAA\xAA\xAA'    #sn 17 U-235
    ]

for peer in peers:
    e.add_peer(peer)
    sleep(.050)
    






def send_msg(_msg):
    for peer in peers:
        e.send(peer, _msg, False)
        print(_msg)
    sleep(interval)


#map function to conver joystic 0..4096 into usable range
def _map(x, in_min, in_max, out_min, out_max):              
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)










#buttons functions
# Define the joystick modes - Button 1
tiltshift_modes = ['tilt','shift']
current_tiltshift_mode_index = 0

# Function to change CE_modes
def change_tiltshift_mode():
    global current_tiltshift_mode_index
    # Increment the mode index
    current_tiltshift_mode_index += 1
    # Wrap around if it exceeds the number of height_modes
    if current_tiltshift_mode_index >= len(tiltshift_modes):
        current_tiltshift_mode_index = 0


# Define the steering modes - Button 4
steersides_modes = ['steer','sides']
current_steersides_mode_index = 0

# Function to change steersides
def change_steersides_mode():
    global current_steersides_mode_index, steersides_modes
    # Increment the mode index
    current_steersides_mode_index += 1
    # Wrap around if it exceeds the number of steersides
    if current_steersides_mode_index >= len(steersides_modes):
        current_steersides_mode_index = 0


# Define the height_modes - button 5
height_modes = ['low', 'standard', 'high']
current_height_mode_index = 0

# Function to change mode
def change_height_mode():
    global current_height_mode_index
    # Increment the mode index
    current_height_mode_index += 1
    # Wrap around if it exceeds the number of height_modes
    if current_height_mode_index >= len(height_modes):
        current_height_mode_index = 0
#     print("Current Height Mode:", height_modes[current_height_mode_index])
  
  
# Define the Collapse_Expand_  button 0 joystick press
ce_modes = ['expand', 'collapse']
current_ce_mode_index = 0

# Function to change CE_modes
def change_ce_mode():
    global current_ce_mode_index
    # Increment the mode index
    current_ce_mode_index += 1
    # Wrap around if it exceeds the number of height_modes
    if current_ce_mode_index >= len(ce_modes):
        current_ce_mode_index = 0
#     print("Current CE Mode:", ce_modes[current_ce_mode_index])

# Initialize joystick and buttons
x_axis = ADC(Pin(35))  
x_axis.atten(ADC.ATTN_11DB)

y_axis = ADC(Pin(34))
y_axis.atten(ADC.ATTN_11DB)

button0 = Pin(32, Pin.IN, Pin.PULL_UP) 
button1 = Pin(14, Pin.IN, Pin.PULL_UP) 
button2 = Pin(27, Pin.IN, Pin.PULL_UP) 
button3 = Pin(26, Pin.IN, Pin.PULL_UP) 
button4 = Pin(25, Pin.IN, Pin.PULL_UP) 
button5 = Pin(33, Pin.IN, Pin.PULL_UP)




def button0_handler():
    if not button0.value():
        change_ce_mode()
        current_ce_mode = ce_modes[current_ce_mode_index]
            
        if current_ce_mode == 'expand':
    #         print('CE expand')
            send_msg("ce_value:100")
            send_msg("gait:WALK")
            
        elif current_ce_mode == 'collapse':
    #         print('CE collapse')
            send_msg("gait:CE")
            send_msg("ce_value:5")
    
        
    
def button1_handler():
    if not button1.value():
        change_tiltshift_mode()
        current_tiltshift_mode = tiltshift_modes[current_tiltshift_mode_index]
        if current_tiltshift_mode == 'tilt':
            send_msg("J_mode:tilt")
            
        elif current_tiltshift_mode == 'shift':
            send_msg("J_mode:shift")
            
            
        
    
    
    
def button2_handler():
    if not button2.value():
        print('wave right leg')
        
        send_msg("gait:wavr")
        


    
def button3_handler():
    if not button3.value():
        
        print('wave left leg')
        
        send_msg("gait:wavl")
        
        

    
def button4_handler():
    if not button4.value():
        print('stering mode switch steersides (btn4 - left)')

        change_steersides_mode()
        current_steersides_mode = steersides_modes[current_steersides_mode_index]
        if current_steersides_mode == 'steer':
            print('mode steer')
            send_msg("J_mode:steer")
            send_msg("gait:WALK")
            
        elif current_steersides_mode == 'sides':
            print('mode sides')
            send_msg("J_mode:sides")
            send_msg("gait:WALK")
                
                




def button5_handler():
    if not button5.value():
        send_msg("gait:WALK")
        sleep(interval)
        
        change_height_mode()
        current_height_mode = height_modes[current_height_mode_index]
        if current_height_mode == 'low':
            print('mode low')
            send_msg("height:80")
            sleep(interval)
            send_msg("raise:40")
            sleep(interval)
            send_msg("spread:105")
            #sleep(interval)
            
        elif current_height_mode == 'standard':
            print('mode standard')
            send_msg("height:120")
            sleep(interval)
            send_msg("raise:55")
            sleep(interval)
            send_msg("spread:110")
            #sleep(interval)
            
        elif current_height_mode == 'high':
            print('mode high')
            send_msg("height:150")
            sleep(interval)
            send_msg("raise:80")
            sleep(interval)
            send_msg("spread:85")
            #sleep(interval)
            

                
     




# Function to read Joystick Inputs and send a message

last_j_x = 0
last_j_y = 0

def read_inputs():
    global last_j_x, last_j_y
    
    
    x_value = x_axis.read()
    y_value = y_axis.read()
    
    
    #Calibrate Joistick here
    j_x = _map(x_value, 110, 3650, -100, 100)
    j_y = _map(y_value, -150-100, 4095+100, 100, -100)
    
    if abs(j_x)<4:
        j_x = 0
    if abs(j_y)<4:
        j_y = 0
        
        
#     print(f"Joystick ADC values: ({x_value}, {y_value})")
    
    if (j_x != last_j_x) or (j_y != last_j_y):
        send_msg(f"J_XY:{j_x}|{j_y}")

        
        last_j_x = j_x
        last_j_y = j_y
    else:
        send_msg(f"J_XY:{j_x}|{j_y}")
        sleep(interval*2)


#setting up initial robot state
print('setup initial robot state')

sleep(interval)
send_msg("gait:WALK")
sleep(interval)
send_msg("J_mode:steer")




while True:
    read_inputs()
    button0_handler()
    button1_handler()
    button2_handler()
    button3_handler()
    button4_handler()
    button5_handler()
    
    
    
