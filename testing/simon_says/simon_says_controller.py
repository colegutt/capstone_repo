# YELLOW LED:    GPIO 17
# RED LED:       GPIO 27
# GREEN LED:     GPIO 22

import RPi.GPIO as GPIO
from time import sleep
import random
from bluetooth import *

def light_up_led(pin, sleep_time):
   GPIO.output(pin, GPIO.HIGH) 
   sleep(sleep_time)
   GPIO.output(pin, GPIO.LOW)

def light_up_led_as_long_as_pressed(client_sock, led, button):
        GPIO.output(led, GPIO.HIGH) 
        while not ('none' in button):
            data = client_sock.recv(1024)
            button = data.decode("utf-8")
            sleep(0.01)
        GPIO.output(led, GPIO.LOW) 
    
def main():

    GPIO.setmode(GPIO.BCM)

    yellow_led = 17
    red_led = 27
    green_led = 22

    # Bluetooth setup
    port = 1
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(("", port))
    server_sock.listen(1)
    print("Waiting for a connection from CTLR...")
    
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

    pin_dict = {
        yellow_led: 'yellow',
        red_led: 'red',
        green_led: 'green'
    }

    # Initialize pins
    GPIO.setup(yellow_led, GPIO.OUT)
    GPIO.setup(red_led, GPIO.OUT)
    GPIO.setup(green_led, GPIO.OUT)
    
    # Make sure all LEDs are off
    GPIO.output(yellow_led, GPIO.LOW)
    GPIO.output(red_led, GPIO.LOW)
    GPIO.output(green_led, GPIO.LOW)

    # Initialize game parameters
    game_is_playing = True
    num_round = 0
    led_sequence = []

    print("BEGIN GAME")

    while game_is_playing:
        num_round = num_round + 1
        print("ROUND ", num_round)
        random_led = random.choice(list(pin_dict.keys()))
        led_sequence.append(random_led)

        # Light up LED sequence
        print("Showing LED sequence")
        for led in led_sequence:
            sleep(0.5)
            light_up_led(led, 0.5)
        
        # Get user input from Bluetooth
        print("Repeat LED sequence")
        i = 0
        while i < len(led_sequence):
            try:
                data = client_sock.recv(1024)
                if not data:
                    print("Connection closed.")
                    game_is_playing = False
                    break
                
                received_button = data.decode("utf-8")
                if 'none' in received_button:
                    continue

                print(f"Received button press: {received_button}")

                light_up_led_as_long_as_pressed(client_sock, led_sequence[i], received_button)
                
                # Check if the received button matches the expected LED in the sequence
                if pin_dict[led_sequence[i]] != received_button:
                    game_is_playing = False
                    break
                
                i += 1
                sleep(0.5)

            except Exception as e:
                print(f"An error occurred while receiving data: {e}")
                game_is_playing = False
                break

        sleep(0.5)

        if game_is_playing:
            print("CORRECT")
            for _ in range(3):
                GPIO.output(yellow_led, GPIO.HIGH)
                GPIO.output(red_led, GPIO.HIGH)
                GPIO.output(green_led, GPIO.HIGH)
                sleep(0.1)
                GPIO.output(yellow_led, GPIO.LOW)
                GPIO.output(red_led, GPIO.LOW)
                GPIO.output(green_led, GPIO.LOW)
                sleep(0.1)
        else:
            print("INCORRECT SEQUENCE. GAME OVER!")
            for _ in range(5):
                light_up_led(red_led, 0.05)
                sleep(0.05)
    
    # Cleanup on game end
    client_sock.close()
    server_sock.close()
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
