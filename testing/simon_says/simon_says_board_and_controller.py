import RPi.GPIO as GPIO
from time import sleep
import random
from bluetooth import *

def light_up_led(pin, sleep_time):
    GPIO.output(pin, GPIO.HIGH)
    sleep(sleep_time)
    GPIO.output(pin, GPIO.LOW)

def light_up_led_as_long_as_pressed(led, button):
    GPIO.output(led, GPIO.HIGH)
    while GPIO.input(button) == GPIO.LOW:
        sleep(0.01)
    GPIO.output(led, GPIO.LOW)

def light_up_led_as_long_as_pressed_controller(client_sock, led, button):
    GPIO.output(led, GPIO.HIGH)
    while not ('none' in button):
        data = client_sock.recv(1024)
        button = data.decode("utf-8")
        sleep(0.01)
    GPIO.output(led, GPIO.LOW)

def connect_bluetooth():
    try:
        port = 1

        # Create a Bluetooth socket
        server_sock = BluetoothSocket(RFCOMM)
        server_sock.bind(("", port))
        server_sock.listen(1)
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from", client_info)
        return client_sock, server_sock
    except BluetoothError as e:
        print(f"Bluetooth not connected: {e}")
        return None, None

def main():
    GPIO.setmode(GPIO.BCM)

    # GPIO pins setup
    yellow_led, red_led, green_led = 17, 27, 22
    yellow_button, red_button, green_button = 18, 15, 14

    pin_dict = {yellow_led: yellow_button, red_led: red_button, green_led: green_button}
    color_dict = {yellow_led: 'yellow', red_led: 'red', green_led: 'green'}
    button_dict = {
        'green': green_button,
        'red': red_button,
        'yellow': yellow_button
    }

    GPIO.setup([yellow_led, red_led, green_led], GPIO.OUT)
    GPIO.setup([yellow_button, red_button, green_button], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Ensure LEDs are off initially
    GPIO.output([yellow_led, red_led, green_led], GPIO.LOW)

    # Game parameters
    game_is_playing = True
    led_sequence = []
    num_round = 0

    # Bluetooth controller connection
    client_sock, server_sock = connect_bluetooth()

    print("BEGIN GAME")

    while game_is_playing:
        num_round += 1
        print(f"ROUND {num_round}")
        random_led = random.choice(list(pin_dict.keys()))
        led_sequence.append(random_led)

        # Show LED sequence
        print("Showing LED sequence")
        for led in led_sequence:
            sleep(0.5)
            light_up_led(led, 0.5)

        # Wait for user input from either board or controller
        print("Repeat LED sequence")
        i = 0
        while i < len(led_sequence):
            user_input = False
            pressed_button = None

            # Check for board input
            for led, button in pin_dict.items():
                if GPIO.input(button) == GPIO.LOW:
                    light_up_led_as_long_as_pressed(led, button)
                    pressed_button = button
                    user_input = True

            # Check for Bluetooth input if connected
            if client_sock:
                data = client_sock.recv(1024)
                if data:
                    received_button = data.decode("utf-8")
                    if not ('none' in received_button):
                        light_up_led_as_long_as_pressed_controller(client_sock, led_sequence[i], received_button)
                        user_input = True
                        pressed_button = button_dict[received_button]

            if user_input:
                if (pressed_button is None) or (pin_dict[led_sequence[i]] != pressed_button):
                    game_is_playing = False
                    break
                i += 1
                sleep(0.5)

        if game_is_playing:
            print("CORRECT")
            for _ in range(3):
                GPIO.output([yellow_led, red_led, green_led], GPIO.HIGH)
                sleep(0.1)
                GPIO.output([yellow_led, red_led, green_led], GPIO.LOW)
                sleep(0.1)
        else:
            print("INCORRECT SEQUENCE. GAME OVER!")
            for _ in range(5):
                light_up_led(red_led, 0.05)
                sleep(0.05)

        # Attempt to reconnect Bluetooth if it was disconnected
        if not client_sock:
            print('trying to connect to bluetooth')
            client_sock, server_sock = connect_bluetooth()

    # Cleanup
    if client_sock:
        client_sock.close()
    if server_sock:
        server_sock.close()
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
