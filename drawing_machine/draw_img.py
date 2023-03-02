from xarm.wrapper import XArmAPI
from G_Sketch import *

def draw_img(img_path):
    arm = XArmAPI('192.168.1.153')

    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)

    sketch = Sketch(img_path)
    # sketch.set_min_distance(1)
    coords = sketch.get_raw_coords()
                     
    workspace = (256, 100, 320, -100)

    workspace_width = workspace[2] - workspace[0]
    workspace_height = abs(workspace[3] - workspace[1])
        
    # Compute the aspect ratio of the workspace
    workspace_aspect_ratio = workspace_width / workspace_height
        
    # Map each coordinate to fit inside the workspace while maintaining the same aspect ratio
    new_coords = []
    for coord in coords:
        # Compute the scaling factor for the coordinate
        coord_scale = min(workspace_width / max(abs(coord[0] - workspace[0]), abs(coord[0] - workspace[2])), 
                              workspace_height / max(abs(coord[1] - workspace[1]), abs(coord[1] - workspace[3])))
            
        # Compute the new coordinates
        new_x = round((coord[0] - workspace[0]) * coord_scale + workspace[0])
        new_y = round((coord[1] - workspace[1]) * coord_scale + workspace[1])
            
        new_coords.append((new_x, new_y))


    print(new_coords)
    coords = new_coords

    for coord in coords:
        arm.set_position(x=coord[0], y=coord[1], wait=True)

        
