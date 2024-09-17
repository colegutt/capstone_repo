import smbus2 as smbus
import time, math

# MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x68
GYRO_YOUT_H = 0x68
GYRO_ZOUT_H = 0x68

# Initialize the MPU6050
def MPU_Init():
    # Write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    # Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    # Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

# Read raw data from the sensor
def read_raw_data(addr):
    # Accelero and Gyro values are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    # Combine high and low values
    value = ((high << 8) | low)
    
    # Convert to signed value (two's complement)
    if value > 32768:
        value = value - 65536
    return value

def determine_orientation(accel_data):
    x, y, z = accel_data
   
    magnitude = math.sqrt(x**2 + y**2 + z**2)
   
    x_norm = x / magnitude
    y_norm = y / magnitude
    z_norm = z / magnitude
   
    threshold_angle = math.pi / 4
   
    tilt_angle_z = math.acos(abs(z_norm))
    tilt_angle_y = math.acos(abs(y_norm))

    if tilt_angle_z < threshold_angle or tilt_angle_y > threshold_angle:
        return "Horizontal"
    else:
        return "Vertical"

bus = smbus.SMBus(1) 
Device_Address = 0x68  

MPU_Init()

while True:
    print("Reading Data from MPU6050...")
    accel_data = (read_raw_data(ACCEL_XOUT_H), read_raw_data(ACCEL_YOUT_H), read_raw_data(ACCEL_ZOUT_H))
    print(accel_data)
    orientation = determine_orientation_gpt(accel_data)
    print(orientation)
    time.sleep(1)