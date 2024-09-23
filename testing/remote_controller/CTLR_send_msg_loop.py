from bluetooth import *
import RPi.GPIO as GPIO
from time import sleep

# Define the MAC address of the MAIN device
main_mac_address = "D8:3A:DD:75:85:23"  # Replace with MAIN's MAC address
port = 1

def connect_to_main():
    """Function to attempt connection to the MAIN device."""
    sock = BluetoothSocket(RFCOMM)
    connected = False
    while not connected:
        try:
            print("Trying to connect to MAIN...")
            sock.connect((main_mac_address, port))
            print("Connected to MAIN")
            connected = True
        except BluetoothError as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            sleep(5)
    return sock

def wait_for_button_release(button):
    """Wait for the button to be released."""
    while GPIO.input(button) == GPIO.LOW:
        sleep(0.1)
    return

try:
    # Initial connection to MAIN
    sock = connect_to_main()

    # GPIO setup
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
        try:
            # Check for button presses and send the corresponding message
            if GPIO.input(red_button) == GPIO.LOW:
                message = 'red'
                sock.send(message)
                print("Message sent: red")
                wait_for_button_release(red_button)
            elif GPIO.input(orange_button) == GPIO.LOW:
                message = 'orange'
                sock.send(message)
                print("Message sent: orange")
                wait_for_button_release(orange_button)
            elif GPIO.input(yellow_button) == GPIO.LOW: 
                message = 'yellow'
                sock.send(message)
                print("Message sent: yellow")
                wait_for_button_release(yellow_button)
            elif GPIO.input(green_button) == GPIO.LOW: 
                message = 'green'
                sock.send(message)
                print("Message sent: green")
                wait_for_button_release(green_button)
            elif GPIO.input(blue_button) == GPIO.LOW: 
                message = 'blue'
                sock.send(message)
                print("Message sent: blue")
                wait_for_button_release(blue_button)
            elif GPIO.input(purple_button) == GPIO.LOW: 
                message = 'purple'
                sock.send(message)
                print("Message sent: purple")
                wait_for_button_release(purple_button)

        except (BluetoothError, OSError) as e:
            # If there's an error (e.g., connection lost), attempt to reconnect
            print(f"Connection lost: {e}. Attempting to reconnect...")
            sock.close()  # Close the current socket
            sock = connect_to_main()  # Reconnect to MAIN

        sleep(0.1)  # Delay to avoid excessive CPU usage

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the socket and clean up GPIO on exit
    if sock:
        sock.close()
    GPIO.cleanup()
