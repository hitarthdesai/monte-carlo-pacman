#this peice of code continuosly returns a word based off of how large the sensor value is
#this is the first draft

#some random code

import board
import busio
import adafruit_vl53l0x
i2c = busio.I2C(board.SCL, board.SDA)
sensor1 = adafruit_vl53l0x.VL53L0X(i2c)
sensor2 = adafruit_vl53l0x.VL53L0X(i2c)
sensor3 = adafruit_vl53l0x.VL53L0X(i2c)

while True:
    if(sensor1.range<3):
        print("Sensor 1: close")
    elif(sensor1.range>=3 and sensor1.range<=7):
        print("Sensor 1: ok")
    else:
        print("Sensor 1: far")
    if(sensor2.range<3):
        print("Sensor 2: close")
    elif(sensor2.range>=3 and sensor2.range<=7):
        print("Sensor 2: ok")
    else:
        print("Sensor 2: far")
    if(sensor3.range<3):
        print("Sensor 3: close")
    elif(sensor3.range>=3 and sensor3.range<=7):
        print("Sensor 3: ok")
    else:
        print("Sensor 3: far")
