import I2C
import pin 
from adafruit_vl53l0x import VL53L0X
I2C_bus = I2C(id=0, board.sda, board.scl) #I2C connection
tof = VL53L0X(I2C_bus) #connecting the VL53L0X to the I2C connection
while True:
    tof.start()
    print(tof.range(), " mm")
    tof.stop()
