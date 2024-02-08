from gpiozero import Motor, RotaryEncoder
from time import sleep

# Motor driver connections
motorN = Motor(forward=17, backward=27)
motorE = Motor(forward=10, backward=9)
motorS = Motor(forward=0, backward=5)
motorW = Motor(forward=13, backward=19)

# Quadrature encoder connections
encoderN = RotaryEncoder(14, 15, max_steps=2500, wrap=True)
encoderE = RotaryEncoder(23, 24, max_steps=2500, wrap=True)
encoderS = RotaryEncoder(1, 12, max_steps=2500, wrap=True)
encoderW = RotaryEncoder(16, 20, max_steps=2500, wrap=True)

wheel_diameter = 1.850394
wheel_circumf = 3.141593 * wheel_diameter
steps_per_rev = 90
steps_per_block = (7 * steps_per_rev) / wheel_circumf
