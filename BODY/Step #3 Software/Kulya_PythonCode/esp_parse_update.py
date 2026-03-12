# Import the esp_context module
import esp_context
from math import sin, cos, radians, sqrt, atan2, pi
import math



def log_scale_map(in_min, in_max, out_min, out_max, x):
    # Step 1: Shift the input range to be positive
    shift = abs(in_min) + 1  # Ensure all values are positive
    shifted_in_min = in_min + shift
    shifted_in_max = in_max + shift
    
    # Step 2: Apply the absolute value and logarithmic transformation
    def log_transform(value):
        shifted_value = abs(value + shift)
        return math.log(shifted_value)
    
    log_min = log_transform(in_min)
    log_max = log_transform(in_max)

    # Step 3: Scale and shift the logarithmic values to the output range
    log_value = log_transform(x)
    scaled_value = ((log_value - log_min) / (log_max - log_min)) * (out_max - out_min) + out_min

    return scaled_value


def parse_and_update(param_string):
    # Split the string into individual param:value pairs
    pairs = param_string.split(';')
    
    for pair in pairs:
        # Skip empty pairs (which can occur with trailing semicolons)
        if not pair.strip():
            continue
        
        # Ensure the pair contains exactly one colon
        if ':' in pair:
            param, value = pair.split(':', 1)  # Split only at the first colon
            try:
                # Convert value to integer (or other appropriate type if needed)
                if value.isdigit():
                    value = int(value)
                
                # Update the RC_data dictionary with the new value
                if param in esp_context.RC_data:
                    esp_context.RC_data[param] = value
                
                if param == "J_XY":
                    J_x, J_y = value.split('|',1)
                        # Convert to integers
                    J_x = int(J_x)
                    J_y = int(J_y)
                    

                    
                    
                    #transform to polar coordinates
                    radius = round(sqrt(J_x**2+J_y**2))
                    theta  = round(atan2(J_y,J_x))
                                  
                    if (radius >100):
                        radius = 100 #should be the max possible value from RC app
                    
                    #calculating cortesian paramets from polar coordinates    
                    J_x = round(radius * cos(theta))
                    J_y = round(radius * sin(theta))
                    
                    print(f"J_x {J_x}   J_y {J_y}")
                     
                    if esp_context.RC_data["J_mode"] == "sides":

                            esp_context.RC_data["dx"] = J_x * .45
                            esp_context.RC_data["dy"] = J_y * .45
                            esp_context.RC_data["speed"] = abs(radius * 1)
                            esp_context.RC_data["turn_angle"] = 0  

#                     if esp_context.RC_data["J_mode"] == "combo":
# 
#                             if J_y > 0:
#                                 esp_context.RC_data["dx"] = -J_x * .2
#                                 esp_context.RC_data["turn_angle"] = -round(J_x * .11)
#                             else: #whe moving backward flip the sides of turn
#                                 esp_context.RC_data["dx"] = J_x * .2
#                                 esp_context.RC_data["turn_angle"] = round(J_x * .11)
#                                 
#                             esp_context.RC_data["speed"] = abs(radius * 1)#abs(J_y * 1)#
#                             esp_context.RC_data["dy"] = J_y * .42
                                
                    if esp_context.RC_data["J_mode"] == "steer":
                            
                         
                            esp_context.RC_data["turn_angle"] = round(J_x * .10)   
                            esp_context.RC_data["dx"] = 0
                            esp_context.RC_data["dy"] = int(J_y) * .45
                            esp_context.RC_data["speed"] = abs(radius * 1)   #abs(J_y * 1)                             

                    if esp_context.RC_data["J_mode"] == "shift":
                            
                            esp_context.RC_data["dx"] = J_x * .45
                            esp_context.RC_data["dy"] = J_y * .45
                            esp_context.RC_data["speed"] = 0
                            esp_context.RC_data["turn_angle"] = 0
                            esp_context.motion_smooth_rate = .35
                    
                    
                    if esp_context.RC_data["J_mode"] == "tilt":
                            
                            esp_context.RC_data["rx"] = J_x * .35
                            esp_context.RC_data["ry"] = J_y * .35
                            esp_context.RC_data["speed"] = 0
                            esp_context.RC_data["turn_angle"] = 0
                            esp_context.motion_smooth_rate = .55
                            

                    print("dx: ", esp_context.RC_data["dx"]," dy: ", esp_context.RC_data["dy"]," speed: ", esp_context.RC_data["speed"]," turn_angle: ", esp_context.RC_data["turn_angle"])
            except ValueError:
                print(f"Warning: Invalid value for {param}. Skipping this pair.")
            
        else:
            print(f"Warning: Skipping invalid pair '{pair}'.")
        
        
# Example usage
# param_string = "dx:0"
# parse_and_update(param_string)
# print(esp_context.RC_data)
# 
# param_string = "dx:0;dy:5;height:6"
# parse_and_update(param_string)
# print(esp_context.RC_data)
# 
# param_string = "dx:0;"
# parse_and_update(param_string)
# print(esp_context.RC_data)