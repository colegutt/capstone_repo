import time 

mpu6050 = mpu6050(0x68)


def read_sensor_data():
    accelerometer_data = mpu6050.get_accel_data()

    gyroscope_data = mpu6050.get_gyro_data()

    temperature = mpu6050.get_temp()

    return accelerometer_data, gyroscope_data, temperature


while True:
    accelerometer_data, gyroscope_data, temperature = read_sensor_data()

    print("Accelerometer Data:", accelerometer_data)
    print("Gyroscope data:", gyroscope_data)
    print("Temp:", temperature)

    time.sleep(1)
