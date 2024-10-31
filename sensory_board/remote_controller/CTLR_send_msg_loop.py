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
            # print(f'[Try {i}]: Trying to connect to MAIN')
            sock.connect((main_mac_address, port))
            # print("Successfully connected to MAIN")
            connected = True
        except BluetoothError as e:
            # print(f"Connection failed: {e}. Retrying in 1 second...")
            sleep(1)
            GPIO.output(button_and_led_dict['connection_led'], GPIO.LOW)
            sleep(1)
    return sock

def wait_for_button_release(button):
    while GPIO.input(button) == GPIO.LOW:
        sleep(0.1)
    return

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)

    heart_button = 25
    circle_button = 24
    star_button = 23
    square_button = 4
    cloud_button = 27
    triangle_button = 22
    connection_led = 13

    GPIO.setup(heart_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(circle_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(star_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(square_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(cloud_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(triangle_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(connection_led, GPIO.OUT)

    return {
        'heart': heart_button,
        'circle': circle_button,
        'star': star_button,
        'square': square_button,
        'cloud': cloud_button,
        'triangle': triangle_button,
        'connection_led': connection_led
    }

def is_socket_connected(sock, button_and_led_dict):
    try:
        ready_to_read = select.select([sock], [], [], 0.1)[0]
        if ready_to_read:
            # Attempt to read data
            data = sock.recv(1024)
            if len(data) == 0:
                # print("Socket disconnected")
                return False
    except BluetoothError as e:
        # print(f"Socket error: {e}")
        return False
    return True

try:
    button_and_led_dict = initialize_gpio()
    sock = connect_to_main(button_and_led_dict)

    while True:
        # Check if the socket is still conn
        if not is_socket_connected(sock, button_and_led_dict):
            # print("Detected disconnection. Attempting to reconnect...")
            sock.close()
            sock = connect_to_main(button_and_led_dict)

        try:
            # Check for button presses and send the corresponding message
            if GPIO.input(button_and_led_dict['heart']) == GPIO.LOW:
                sock.send('heart')
                # print("Message sent: heart")
                wait_for_button_release(button_and_led_dict['heart'])
            elif GPIO.input(button_and_led_dict['circle']) == GPIO.LOW:
                sock.send('circle')
                # print("Message sent: circle")
                wait_for_button_release(button_and_led_dict['circle'])
            elif GPIO.input(button_and_led_dict['star']) == GPIO.LOW: 
                sock.send('star')
                # print("Message sent: star")
                wait_for_button_release(button_and_led_dict['star'])
            elif GPIO.input(button_and_led_dict['square']) == GPIO.LOW: 
                sock.send('square')
                # print("Message sent: square")
                wait_for_button_release(button_and_led_dict['square'])
            elif GPIO.input(button_and_led_dict['cloud']) == GPIO.LOW: 
                sock.send('cloud')
                # print("Message sent: cloud")
                wait_for_button_release(button_and_led_dict['cloud'])
            elif GPIO.input(button_and_led_dict['triangle']) == GPIO.LOW: 
                sock.send('triangle')
                # print("Message sent: triangle")
                wait_for_button_release(button_and_led_dict['triangle'])

        except (BluetoothError, OSError) as e:
            # print(f"Connection lost: {e}. Attempting to reconnect...")
            sock.close()
            sock = connect_to_main(button_and_led_dict)

        sleep(0.1)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # if sock:
    #     sock.close()
    GPIO.cleanup()
