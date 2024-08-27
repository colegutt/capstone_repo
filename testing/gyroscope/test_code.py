import smbus2 as smbus
import time

# MPU6050 Registers and Addresses
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
TEMP_OUT_H = 0x41

# MPU6050 Initialization
def MPU_Init():
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 0)  # Wake up the MPU6050

def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)
    value = (high << 8) | low
    if value > 32768:
        value -= 65536
    return value

def read_sensor_data():
    accel_x = read_raw_data(ACCEL_XOUT_H)
    accel_y = read_raw_data(ACCEL_XOUT_H + 2)
    accel_z = read_raw_data(ACCEL_XOUT_H + 4)

    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_XOUT_H + 2)
    gyro_z = read_raw_data(GYRO_XOUT_H + 4)

    temp = read_raw_data(TEMP_OUT_H)

    # Convert temperature to degrees Celsius
    temp = (temp / 340.0) + 36.53

    accelerometer_data = {'x': accel_x, 'y': accel_y, 'z': accel_z}
    gyroscope_data = {'x': gyro_x, 'y': gyro_y, 'z': gyro_z}

    return accelerometer_data, gyroscope_data, temp

# Setup
bus = smbus.SMBus(1)  # or 0 if you're using an older Raspberry Pi model
Device_Address = 0x68  # MPU6050 device address

MPU_Init()

while True:
    accelerometer_data, gyroscope_data, temperature = read_sensor_data()

    print("Accelerometer Data:", accelerometer_data)
    print("Gyroscope Data:", gyroscope_data)
    print("Temperature:", temperature)

    time.sleep(1)
