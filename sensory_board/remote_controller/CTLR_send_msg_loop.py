from bluetooth import *
import RPi.GPIO as GPIO
from time import sleep
import select

# This script is continuously ran on the remote game controller as long as the controller is on

main_mac_address = "D8:3A:DD:75:85:23"
port = 1

def connect_to_main(button_and_led_dict):
    connected = False
    i = 0
    while not connected:
        GPIO.output(button_and_led_dict['connection_led'], GPIO.HIGH)
        try:
            i += 1
            sock = BluetoothSocket(RFCOMM)
            print(f'[Try {i}]: Trying to connect to MAIN')
            sock.connect((main_mac_address, port))
            print("Successfully connected to MAIN")
            connected = True
        except BluetoothError as e:
            print(f"Connection failed: {e}. Retrying in 1 second...")
            sleep(0.5)
            GPIO.output(button_and_led_dict['connection_led'], GPIO.LOW)
            sleep(0.5)
    return sock

def wait_for_button_release(button):
    while GPIO.input(button) == GPIO.LOW:
        sleep(0.1)
    return

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)

    red_button = 25
    orange_button = 24
    yellow_button = 23
    green_button = 4
    blue_button = 27
    purple_button = 22
    connection_led = 13

    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(orange_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(blue_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(purple_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(connection_led, GPIO.OUT)

    return {
        'red': red_button,
        'orange': orange_button,
        'yellow': yellow_button,
        'green': green_button,
        'blue': blue_button,
        'purple': purple_button,
        'connection_led': connection_led
    }

def is_socket_connected(sock, button_and_led_dict):
    try:
        ready_to_read = select.select([sock], [], [], 0.1)[0]
        if ready_to_read:
            # Attempt to read data
            data = sock.recv(1024)
            if len(data) == 0:
                print("Socket disconnected")
                return False
    except BluetoothError as e:
        print(f"Socket error: {e}")
        return False
    return True

try:
    button_and_led_dict = initialize_gpio()
    sock = connect_to_main(button_and_led_dict)

    while True:
        # Check if the socket is still conn
        if not is_socket_connected(sock, button_and_led_dict):
            print("Detected disconnection. Attempting to reconnect...")
            sock.close()
            sock = connect_to_main(button_and_led_dict)

        try:
            # Check for button presses and send the corresponding message
            if GPIO.input(button_and_led_dict['red']) == GPIO.LOW:
                sock.send('red')
                print("Message sent: red")
                wait_for_button_release(button_and_led_dict['red'])
            elif GPIO.input(button_and_led_dict['orange']) == GPIO.LOW:
                sock.send('orange')
                print("Message sent: orange")
                wait_for_button_release(button_and_led_dict['orange'])
            elif GPIO.input(button_and_led_dict['yellow']) == GPIO.LOW: 
                sock.send('yellow')
                print("Message sent: yellow")
                wait_for_button_release(button_and_led_dict['yellow'])
            elif GPIO.input(button_and_led_dict['green']) == GPIO.LOW: 
                sock.send('green')
                print("Message sent: green")
                wait_for_button_release(button_and_led_dict['green'])
            elif GPIO.input(button_and_led_dict['blue']) == GPIO.LOW: 
                sock.send('blue')
                print("Message sent: blue")
                wait_for_button_release(button_and_led_dict['blue'])
            elif GPIO.input(button_and_led_dict['purple']) == GPIO.LOW: 
                sock.send('purple')
                print("Message sent: purple")
                wait_for_button_release(button_and_led_dict['purple'])

        except (BluetoothError, OSError) as e:
            print(f"Connection lost: {e}. Attempting to reconnect...")
            sock.close()
            sock = connect_to_main(button_and_led_dict)

        sleep(0.1)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # if sock:
    #     sock.close()
    GPIO.cleanup()
