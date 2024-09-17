from bluetooth import *

# Define the MAC address of the MAIN device
main_mac_address = "D8:3A:DD:75:85:23"  # Replace with MAIN's MAC address

# Define the port and message
port = 1
message = "hello world"

# Create a Bluetooth socket
sock = BluetoothSocket(RFCOMM)

try:
    # Connect to the MAIN device
    sock.connect((main_mac_address, port))
    print("Connected to MAIN. Sending message...")

    # Send the message
    sock.send(message)
    print("Message sent!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the socket
    sock.close()
