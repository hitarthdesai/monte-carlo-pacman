from motor_parameters import *
from motor_control import control_motor_speed

# In this file we will be checking motor calibration
# we will have two
check_dc = False
check_encoder = False

# input from user to check what they want to test
print("What would you like to test?")
print("1. DC motors")
print("2. Encoders")
print("3. Both")
print("4. Quit")
user_input = input("Enter your choice: ")
# use the user input to set the values of check_dc and check_encoder
if user_input == "1":
    check_dc = True
elif user_input == "2":
    check_encoder = True
elif user_input == "3":
    check_dc = True
    check_encoder = True
# 1. dc motor is connected properly
if check_dc:
    print("0.5s movement in each direction")
    motorN.forward()
    sleep(0.5)
    motorN.stop()

    motorS.forward()
    sleep(0.5)
    motorS.stop()

    motorE.forward()
    sleep(0.5)
    motorE.stop()

    motorW.forward()
    sleep(0.5)
    motorW.stop()
    print("dc test is complete")

# 2. encoders are connected and working properly
if check_encoder:
    print("encoder test is starting")
    encoderN.steps = 0
    encoderE.steps = 0
    encoderW.steps = 0
    encoderS.steps = 0
    print("Moving north 1 block using E encoder")
    while abs(encoderE.steps) < steps_per_block:
        # print(f"encoderE.steps: {encoderE.steps}")
        control_motor_speed("N", 1.0)
    print("Moving south 1 block using W encoder")
    while abs(encoderW.steps) < steps_per_block:
        # print(f"encoderW.steps: {encoderW.steps}")
        control_motor_speed("S", 1.0)
    print("Moving east 1 block using N encoder")
    while abs(encoderN.steps) < steps_per_block:
        # print(f"encoderN.steps: {encoderN.steps}")
        control_motor_speed("E", 1.0)
    print("Moving west 1 block using S encoder")
    while abs(encoderS.steps) < steps_per_block:
        # print(f"encoderS.steps: {encoderS.steps}")
        control_motor_speed("W", 1.0)
    print("encoder test is complete")

motorN.stop()
motorE.stop()
motorS.stop()
motorW.stop()
