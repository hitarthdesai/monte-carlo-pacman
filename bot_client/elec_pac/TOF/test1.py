#this peice of code returns a single value from the TOF sensor
#this is the first draft

#some random code

import board
import busio
import adafruit_vl53l0x
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)

print('Range: {}mm'.format(sensor.range))