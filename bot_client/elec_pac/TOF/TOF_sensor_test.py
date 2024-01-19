#Tasks:
#Make continous loop for the tof sensor. The continous reading shouldnt give the mm distance, it should return “close”, “ok” and “far” [that should be based on distance]
#Connect 3 tof sensors and simultaneous readings from all 3 at the same time

#returns a single value from the TOF sensor
import board
import busio
import adafruit_vl53l0x
#import time 

i2c = busio.I2C(board.SCL, board.SDA)

#declare close/far variables
closevar = 200
farvar = 400

sensor1= adafruit_vl53l0x.VL53L0X(i2c)
sensor2= adafruit_vl53l0x.VL53L0X(i2c)
sensor3= adafruit_vl53l0x.VL53L0X(i2c)

#address stuff?
#sensor1_address
#sensor2_address
#sensor3_address

#function that outputs the distance from sensor to object
def checkallsensors():      
        if sensor1.range <= closevar:
                print("Sensor 1 is too close")
        elif sensor1.range < farvar and sensor1.range > closevar:
                print("Sensor 1 is Ok")
        elif sensor1.range >= farvar: 
                print("Sensor 1 is too Far")

        if sensor2.range <= closevar:
                print("Sensor 2 is too close")
        elif sensor2.range < farvar and sensor2.range > closevar:
                print("Sensor 2 is Ok")
        elif sensor2.range >= farvar: 
                print("Sensor 2 is too Far")

        if sensor3.range <= closevar:
                print("Sensor 3 is too close")
        elif sensor3.range < farvar and sensor3.range > closevar:
                print("Sensor 3 is Ok")
        elif sensor3.range >= farvar: 
                print("Sensor 3 is too Far")


        

#put a for loop inside a function
#change the sensor# to keep on checking?
'''def checkallsensors():
        
        for x in range(1,3): 
                if sensor1.range <= closevar:
                        print("Sensor 1 is too close")
                elif sensor1.range < farvar and sensor1.range > closevar:
                        print("Sensor 1 is Ok")
                elif sensor1.range >= farvar: 
                        print("Sensor 1 is too Far")
'''

#while True:
#        checkallsensors()
#        print('Sensor 1 reading is'.format(sensor1.range))
print('Range: {}mm'.format(sensor1.range))
print('Range: {}mm'.format(sensor2.range))
print('Range: {}mm'.format(sensor3.range))
