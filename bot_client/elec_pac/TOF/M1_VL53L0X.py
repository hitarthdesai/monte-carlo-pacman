import time
import smbus

# Define I2C bus (0 for Pi 1, 1 for Pi 2 and newer)
I2C_BUS = 1

# I2C address of the VL53L0X sensor
VL53L0X_ADDRESS = 0x29

# Create an instance of the I2C bus
bus = smbus.SMBus(I2C_BUS)

# VL53L0X register addresses
VL53L0X_REG_RESULT_RANGE_STATUS = 0x14  # Register to check measurement status
VL53L0X_REG_SYSRANGE_START = 0x00  # Register to initiate a measurement

# Initialize the VL53L0X sensor
def setup_vl53l0x():
    # Set the sensor to long-range mode (lower accuracy but longer range)
    bus.write_byte_data(VL53L0X_ADDRESS, 0x01, 0x00)

# Start a distance measurement
def start_measurement():
    bus.write_byte_data(VL53L0X_ADDRESS, VL53L0X_REG_SYSRANGE_START, 0x01)

# Check if a measurement is ready
def is_measurement_ready():
    return (bus.read_byte_data(VL53L0X_ADDRESS, VL53L0X_REG_RESULT_RANGE_STATUS) & 0x01) == 1

# Get the distance measurement
def get_distance():
    return bus.read_word_data(VL53L0X_ADDRESS, 0x14)

if __name__ == "__main__":
    try:
        setup_vl53l0x()
        while True:
            start_measurement()
            while not is_measurement_ready():
                time.sleep(0.01)
            distance = get_distance()
            print(f"Distance: {distance} mm")
            time.sleep(1)  # Add delay for readability
    except KeyboardInterrupt:
        print("Measurement stopped by user")
