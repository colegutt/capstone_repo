from bluetooth import *

# Replace with your gaming console's MAC address
MAC_ADDRESS = 'D8:3A:DD:75:85:23'
PORT = 1

# Create a Bluetooth socket
sock = BluetoothSocket(RFCOMM)
sock.connect((MAC_ADDRESS, PORT))

try:
    while True:
        sock.send("Hello from Remote Controller")
        time.sleep(1)

except IOError:
    pass

sock.close()