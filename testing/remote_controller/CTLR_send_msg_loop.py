from bluetooth import *
import RPi.GPIO as GPIO
from time import sleep

# Define the MAC address of the MAIN device
main_mac_address = "D8:3A:DD:75:85:23"  # Replace with MAIN's MAC address

# Define the port and message
port = 1
message = "hello world"

# Create a Bluetooth socket
sock = BluetoothSocket(RFCOMM)

def wait_for_button_release(button):
    while GPIO.input(button) == GPIO.LOW:
        sleep(0.1)
    return

def connect_bluetooth():
    while True:
        try:
            sock.connect((main_mac_address, port))
            print("Connected to MAIN")
            break
        except Exception as e:
            print(f"Connection failed: {e}. Retrying...")
            sleep(2)  # Wait before retrying

try:
    connect_bluetooth()  # Attempt to connect at the start
    GPIO.setmode(GPIO.BCM)
    
    # Define button pins
    red_button = 25
    orange_button = 24
    yellow_button = 23
    green_button = 4
    blue_button = 27
    purple_button = 22

    # Setup GPIO pins
    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(orange_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(blue_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(purple_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        try:
            if GPIO.input(red_button) == GPIO.LOW:
                message = 'red'
                sock.send(message)
                print("Message sent!")
                wait_for_button_release(red_button)
            elif GPIO.input(orange_button) == GPIO.LOW:
                message = 'orange'
                sock.send(message)
                print("Message sent!")
                wait_for_button_release(orange_button)
            elif GPIO.input(yellow_button) == GPIO.LOW: 
                message = 'yellow'
                sock.send(message)
                print("Message sent!")
                wait_for_button_release(yellow_button)
            elif GPIO.input(green_button) == GPIO.LOW: 
                message = 'green'
                sock.send(message)
                print("Message sent!")
                wait_for_button_release(green_button)
            elif GPIO.input(blue_button) == GPIO.LOW: 
                message = 'blue'
                sock.send(message)
                print("Message sent!")
                wait_for_button_release(blue_button)
            elif GPIO.input(purple_button) == GPIO.LOW: 
                message = 'purple'
                sock.send(message)
                print("Message sent!")
                wait_for_button_release(purple_button)

            sleep(0.1)

        except BluetoothError as e:
            print(f"Bluetooth error occurred: {e}. Reconnecting...")
            sock.close()  # Close the socket before reconnecting
            connect_bluetooth()  # Try to reconnect

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the socket
    sock.close()
