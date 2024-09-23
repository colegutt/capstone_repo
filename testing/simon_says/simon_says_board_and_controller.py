import sys
import simon_says_demo
import RPi.GPIO as GPIO
import threading
from time import sleep
from bluetooth import *

# Global variables
global THREAD_FLAG
THREAD_FLAG = False

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
    simon_says_demo.stop()

def listen_for_bluetooth_input():
    """
    Listens for Bluetooth input from the controller in a separate thread.
    Returns True if input is received, False otherwise.
    """
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
                    print(f"Received Bluetooth input: {data.decode('utf-8')}")
                    # Process Bluetooth input (this will be handled in the game logic)
            except Exception as e:
                print(f"Error receiving Bluetooth input: {e}")
                client_sock = None  # Reset client socket on error

def main_game_logic():
    """
    This starts the Simon Says game logic in a separate thread.
    """
    global THREAD_FLAG
    THREAD_FLAG = False
    demo_thread = threading.Thread(target=simon_says_demo.main)
    demo_thread.start()

def check_board_button():
    """
    Checks if the board button is pressed.
    Returns True if the button is pressed, False otherwise.
    """
    return GPIO.input(start_button) == GPIO.LOW

if __name__ == "__main__":
    try:
        init_gpio()

        # Start listening for Bluetooth connections in a separate thread
        bt_thread = threading.Thread(target=listen_for_bluetooth_input)
        bt_thread.daemon = True
        bt_thread.start()

        # Start the Simon Says game logic immediately
        print("Starting game with board buttons. Bluetooth can connect mid-game.")
        main_game_logic()

        # Main loop to monitor the board button (start button) during the game
        while True:
            # If board button is pressed during the game, it can stop/start the game
            if check_board_button():
                print("Board button pressed.")
                if THREAD_FLAG:
                    # If the game is stopped, restart the game
                    main_game_logic()
                else:
                    # If the game is running, stop it
                    stop_demo()

            sleep(0.15)

    except KeyboardInterrupt:
        stop_demo()
        GPIO.cleanup()
        if client_sock:
            client_sock.close()
        server_sock.close()
