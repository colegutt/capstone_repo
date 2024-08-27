import smbus2 as smbus
import time

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
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

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

# Setup
bus = smbus.SMBus(1)  # or 0 if you're using an older Raspberry Pi model
Device_Address = 0x68  # MPU6050 device address

MPU_Init()

print("Reading Data from MPU6050...")

while True:
    # Read accelerometer data
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    # Read gyroscope data
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    # Print accelerometer data
    print(f"Ax={acc_x}, Ay={acc_y}, Az={acc_z}")

    # Print gyroscope data
    print(f"Gx={gyro_x}, Gy={gyro_y}, Gz={gyro_z}")

    time.sleep(1)