from bluetooth import *
import RPi.GPIO as GPIO

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
    print("Connected to MAIN")
    GPIO.setmode(GPIO.BCM)
    red_button = 25
    orange_button = 24
    yellow_button = 23
    green_button = 4
    blue_button = 27
    purple_button = 22

    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(orange_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(blue_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(purple_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        if GPIO.input(red_button) == GPIO.LOW:
            message = 'red'
            sock.send(message)
            print("Message sent!")
        elif GPIO.input(orange_button) == GPIO.LOW:
            message = 'orange'
            sock.send(message)
            print("Message sent!")
        elif GPIO.input(yellow_button) == GPIO.LOW: 
            message = 'yellow'
            sock.send(message)
            print("Message sent!")
        elif GPIO.input(green_button) == GPIO.LOW: 
            message = 'green'
            sock.send(message)
            print("Message sent!")
        elif GPIO.input(blue_button) == GPIO.LOW: 
            message = 'blue'
            sock.send(message)
            print("Message sent!")
        elif GPIO.input(purple_button) == GPIO.LOW: 
            message = 'purple'
            sock.send(message)
            print("Message sent!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the socket
    sock.close()
