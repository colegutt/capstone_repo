import sys
import RPi.GPIO as GPIO
import threading
from time import sleep
from bluetooth import *
import random

# Global variables
global THREAD_FLAG, expected_sequence, current_index, client_sock
THREAD_FLAG = False
expected_sequence = []
current_index = 0

# GPIO button (Board button) settings
start_button = 10  # GPIO pin for the start button on the board

# Bluetooth setup
port = 1
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", port))
server_sock.listen(1)
client_sock = None  # Global variable to store client connection when Bluetooth is connected

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(start_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def stop_demo():
    global THREAD_FLAG
    THREAD_FLAG = True

def listen_for_bluetooth_input():
    global client_sock
    while True:
        if client_sock is None:
            print("Waiting for a connection from CTLR...")
            try:
                client_sock, client_info = server_sock.accept()
                print("Accepted connection from", client_info)
            except Exception as e:
                print(f"Error accepting Bluetooth connection: {e}")
        else:
            try:
                data = client_sock.recv(1024)
                if data:
                    input_str = data.decode('utf-8')
                    print(f"Received Bluetooth input: {input_str}")
                    process_bluetooth_input(input_str)
            except Exception as e:
                print(f"Error receiving Bluetooth input: {e}")
                client_sock = None  # Reset client socket on error

def generate_sequence():
    return random.choices(['red', 'blue', 'green', 'yellow'], k=5)  # Example sequence length

def process_bluetooth_input(input_str):
    global current_index
    print(f"Processing input from controller: {input_str}")
    if input_str == expected_sequence[current_index]:
        print(f"Correct input: {input_str}")
        current_index += 1
        if current_index >= len(expected_sequence):
            print("Round complete! Generating next sequence.")
            expected_sequence = generate_sequence()
            current_index = 0
    else:
        print(f"Incorrect input: {input_str}. Game over.")
        # Reset game logic here if desired

def process_board_input():
    global current_index
    if GPIO.input(start_button) == GPIO.LOW:
        print("Board button pressed.")
        # Check if the current index is valid and process it
        # This should be modified to check the specific input associated with the board button logic
        # Assuming the board button is red for example
        if expected_sequence[current_index] == 'red':  # Modify this logic based on your actual buttons
            print("Correct input from board.")
            current_index += 1
            if current_index >= len(expected_sequence):
                print("Round complete! Generating next sequence.")
                expected_sequence = generate_sequence()
                current_index = 0
        else:
            print("Incorrect input from board. Game over.")
            # Reset game logic here if desired

def main_game_logic():
    global THREAD_FLAG, expected_sequence, current_index
    THREAD_FLAG = False
    expected_sequence = generate_sequence()
    current_index = 0
    print(f"Starting game with sequence: {expected_sequence}")

    # Main game loop
    while not THREAD_FLAG:
        # Simulate showing the LED sequence here (not implemented in this example)
        for color in expected_sequence:
            print(f"Showing LED: {color}")  # Replace with actual LED control
            sleep(1)  # Show each LED for 1 second

        sleep(1)  # Pause before next round

def check_inputs():
    if client_sock:  # If the controller is connected, process Bluetooth input
        return
    else:  # If not connected, process board input
        process_board_input()

if __name__ == "__main__":
    try:
        init_gpio()

        # Start listening for Bluetooth connections in a separate thread
        bt_thread = threading.Thread(target=listen_for_bluetooth_input)
        bt_thread.daemon = True
        bt_thread.start()

        # Start the game immediately
        print("Starting game. Use board buttons or Bluetooth controller.")
        main_game_logic()

        # Main loop to monitor inputs during the game
        while True:
            check_inputs()  # Check inputs based on connection status
            sleep(0.15)

    except KeyboardInterrupt:
        stop_demo()
        GPIO.cleanup()
        if client_sock:
            client_sock.close()
        server_sock.close()
