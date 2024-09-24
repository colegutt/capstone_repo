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
    while True:
        try:
            data = client_sock.recv(1024)
            if data:
                button = data.decode("utf-8")
                if 'none' not in button:
                    break
        except BluetoothError as e:
            if e.errno == 11:  # Resource temporarily unavailable
                sleep(0.01)
            else:
                print(f'Bluetooth error: {e}')
                break
    GPIO.output(led, GPIO.LOW)

def connect_bluetooth():
    print('Checking for Bluetooth controller...')
    port = 1  # Default RFCOMM port
    server_sock = BluetoothSocket(RFCOMM)

    try:
        server_sock.bind(("", port))
        server_sock.listen(1)
        # server_sock.setblocking(False)  # Set non-blocking mode
        print("Bluetooth socket created and listening.")

        try:
            client_sock, client_info = server_sock.accept()
            print("Accepted connection from", client_info)
            return client_sock, server_sock
        except BluetoothError as e:
            if e.errno == 11:  # Resource temporarily unavailable
                print("No controller connected. Proceeding without Bluetooth controller.")
            else:
                print(f"Bluetooth connection error while accepting: {e}")

    except BluetoothError as e:
        print(f"Bluetooth connection error: {e}")

    return None, server_sock  # Return None for client_sock, keep the server_sock

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

    # Bluetooth controller connection check
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
                # client_sock.setblocking(False)  # Set non-blocking mode
                try:
                    data = client_sock.recv(1024)
                    if data:
                        received_button = data.decode("utf-8")
                        print(received_button)
                        if 'none' not in received_button:
                            light_up_led_as_long_as_pressed_controller(client_sock, led_sequence[i], received_button)
                            user_input = True
                            pressed_button = button_dict[received_button]
                except BluetoothError as e:
                    if e.errno == 11:  # Resource temporarily unavailable
                        pass  # Continue checking for controller input
                    else:
                        print(f'Bluetooth disconnected: {e}')
                        client_sock.close()
                        client_sock = None  # Keep the server socket alive

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
            break

        # Attempt to reconnect Bluetooth if it was disconnected
        if not client_sock:
            print('Rechecking Bluetooth connection...')
            client_sock, server_sock = connect_bluetooth()
            if client_sock is None:
                print("No Bluetooth controller connected. You can continue playing without it.")
                sleep(1)  # Wait before trying again to avoid spamming connections

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
