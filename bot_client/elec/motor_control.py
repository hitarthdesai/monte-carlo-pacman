from motor_parameters import *

def control_motor_speed(direction, speed):
    if direction == "N":
        motorE.backward(speed)
        motorW.forward(speed)
    if direction == "S":
        motorE.forward(speed)
        motorW.backward(speed)
    if direction == "E":
        motorN.forward(speed)
        motorS.backward(speed)
    if direction == "W":
        motorN.backward(speed)
        motorS.forward(speed)


def gradual_speed_change(
    target_steps, direction, encoder, gradual_change=True, rate_of_increase=4
):
    speed = 0.0

    try:
        if gradual_change:
            print("gradual change\n")
            # Gradually increase the speed
            while abs(encoder.steps) < (target_steps / (2 * rate_of_increase)):
                print("loop1\n")
                speed = min(speed + (rate_of_increase / 100.0), 1.0)
                control_motor_speed(direction, speed)
                print("Encoder.steps = ", abs(encoder.steps))
                sleep(0.1)

            # Hold the maximum speed for the remaining time
            while abs(encoder.steps) < (
                target_steps * (1 - (1 / (2 * rate_of_increase)))
            ):
                print("loop2\n")
                control_motor_speed(direction, 1.0)
                print(abs(encoder.steps))
                sleep(0.1)

            # Gradually decrease the speed
            while abs(encoder.steps) < target_steps:
                print("loop3\n")
                speed = max(speed - (rate_of_increase / 100.0), 0.25)
                control_motor_speed(direction, speed)
                print(abs(encoder.steps))
                sleep(0.1)
        else:
            # Hold a constant speed for the entire duration
            print("else statement\n")
            while abs(encoder.steps) < target_steps:
                print("loop4\n")
                control_motor_speed(direction, 1.0)

    except KeyboardInterrupt:
        pass

def move_direction_static(direction, target_steps, encoder1, encoder2):
    while abs(encoder1.steps) < target_steps:
        print("using encoder 1 to move\n")
        control_motor_speed(direction, 1.0)
    
    while abs(encoder2.steps) < target_steps:
        print("using encoder 2 to move\n")
        control_motor_speed(direction, 1.0)


def move_robot(num_blocks, direction, acceleration=4):
    encoderN.steps = 0
    encoderE.steps = 0
    encoderW.steps = 0
    encoderS.steps = 0

    target_steps = int(steps_per_block * num_blocks)

    print(f"Moving {num_blocks} block(s) {direction} without gradual acceleration {acceleration}")
    print(f"Target steps: {target_steps}")

    if direction == "N":
        move_direction_static(direction, encoderE, encoderW)
    elif direction == "S":
        move_direction_static(direction, encoderW, encoderE)
    elif direction == "E":
        move_direction_static(direction, encoderN, encoderS)
    elif direction == "W":
        move_direction_static(direction, encoderS, encoderN)
    
    print("Done moving")
    encoderN.steps = 0
    encoderE.steps = 0
    encoderW.steps = 0
    encoderS.steps = 0
    motorN.stop()
    motorE.stop()
    motorS.stop()
    motorW.stop()

    


def only_dc(num_blocks, direction, acceleration):
    if direction == "N":
        motorN.forward()
        sleep(1)
        motorN.stop()
    if direction == "S":
        motorS.forward()
        sleep(1)
        motorS.stop()
    if direction == "E":
        motorE.forward()
        sleep(1)
        motorE.stop()
    if direction == "W":
        motorW.forward()
        sleep(1)
        motorW.stop()
