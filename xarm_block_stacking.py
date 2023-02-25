from xarm.wrapper import XArmAPI
from position import *
import time

# Init
arm = XArmAPI('192.168.1.153')

arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

arm.set_gripper_enable(enable=True)
arm.set_gripper_mode(0)

# Constant positions representing the ground (ground) and a safe movement zone (air)
ground = 80
air = 140

# Keeping track of current z position
z = 120

# Holds value of what degree will put the gripper at absolute 0
zero_angle = 0

# Moving arm to pose
def go_to(pos):
    global z, zero_angle

    # Setting position 
    arm.set_position(x=pos.x, y=pos.y, z=pos.z, wait=True)

    # Updating current z
    z = pos.z

    #Getting the angle of the first servo (will always be equal to the number of degrees that the gripper is from absolute 0 when at 0
    code, zero_angle = arm.get_servo_angle(servo_id=1)

    # If the angle is 0, returning to absolute 0
    if pos.angle == 0:
        arm.set_servo_angle(servo_id=6, angle=zero_angle, wait=True)

    #Otherwise, moving to specific rotation (not absolute)
    else:
        arm.set_servo_angle(servo_id=6, angle=pos.angle, wait=True)

# Adjusting z and lowering
def lower():
    global z
    z -= 40
    arm.set_position(z=z, wait=True)

# Adjusting z and lifting
def lift():
    global z
    z += 40
    arm.set_position(z=z, wait=True)

# Closing grip
def close_grip():
    arm.close_lite6_gripper()
    time.sleep(1)

# Opening grip
def open_grip():
    arm.open_lite6_gripper()
    time.sleep(1)

# Stops sending commands until the arm stops moving
def wait():
    while arm.get_is_moving():
        pass

# Picks a block up and moves it to the start position
def get_block(a_pos):
    go_to(a_pos)
    lower()
    close_grip() 
    lift()
    go_to(stack_pos)
    lower()
    open_grip()
    lift()
    stack_pos.z += 25
    next_to_stack_pos.z += 25
    go_to(next_to_stack_pos)

# Position to stack to
stack_pos = Position((200, -35, 120), 0)

# Position to move to after stacking (prevents collision)
next_to_stack_pos = Position((200, 35, 120), 0)

# Block positions
a = Position((240, 148, 120), 0)
b = Position((305, 141, 120), 55)
c = Position((305, 74, 120), 60)
d = Position((265, 18, 120), 65)
e = Position((316, 8, 120), 85)
f = Position((207, 55, 120), 0)

blocks = [a, b, c, d, e, f]

# Init
open_grip()
arm.reset(wait=True)

# Picking up all blocks
for block in blocks:
    get_block(block)
    
    # Waiting to prevent command overflow
    wait()

# Disconneting from arm
arm.disconnect()
