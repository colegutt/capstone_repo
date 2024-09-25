import RPi.GPIO as GPIO
from time import sleep
import random
import threading
from general_functions import GeneralFunctions
from bluetooth import BluetoothSocket, BluetoothError, RFCOMM

# Game Parameters
SPEED = 0.5
CTLR_LIGHT_UP_SLEEP_TIME = 0.25

class MemoryGame:
    def __init__(self, multiplayer=False):
        # Initializations
        self.pause_event = threading.Event()
        self.gen_funcs = GeneralFunctions()
        self.end_game = False
        self.player = 1
        self.multiplayer = multiplayer
        self.pin_dict, self.buttons, self.leds = self.gen_funcs.init_gpio()
        self.button_dict = {
            'green': self.buttons[2],
            'red': self.buttons[1],
            'yellow': self.buttons[0]
        }
        self.led_dict = {
            'green': self.leds[2],
            'red': self.leds[1],
            'yellow': self.leds[0],
        }
        self.gen_funcs.turn_off_all_leds()

        # Bluetooth initialization
        self.client_sock, self.server_sock = self.connect_bluetooth()

    def connect_bluetooth(self):
        # print('Checking for Bluetooth controller...')
        port = 1  # Default RFCOMM port
        server_sock = BluetoothSocket(RFCOMM)

        try:
            server_sock.bind(("", port))
            server_sock.listen(1)
            server_sock.setblocking(False)  # Set non-blocking mode
            # print("Bluetooth socket created and listening.")
        except BluetoothError as e:
            # print(f"Bluetooth connection error: {e}")
            return None, server_sock

        # Function to periodically check for Bluetooth connection
        def attempt_accept():
            client_sock = None
            while client_sock is None:
                try:
                    client_sock, client_info = server_sock.accept()
                    # print(f"Accepted connection from {client_info}")
                    self.client_sock = client_sock
                    return client_sock, server_sock
                except BluetoothError as e:
                    if e.errno == 11:  # No connection yet (non-blocking)
                        sleep(0.01)
                        # print("No controller connected. Retrying...")
                    else:
                        # print(f"Bluetooth connection error: {e}")
                        break
                sleep(1)  # Retry every 1 second
            return None, server_sock

        # Start checking for connection in a separate thread
        connection_thread = threading.Thread(target=attempt_accept, daemon=True)
        connection_thread.start()

        return None, server_sock  # Return None for client_sock until connection is made

    # Start memory game
    def run_game(self, update_score_callback, on_game_over_callback, update_player_callback=None):
        game_is_playing = True
        num_round = 0
        led_sequence = []

        while game_is_playing:
            num_round += 1
            led_sequence.append(random.choice(self.leds))

            # Light up LED sequence
            for led in led_sequence:
                if self.wait_to_resume() == 1:
                    GPIO.cleanup()
                    return
                self.gen_funcs.light_up_led_w_sleep(led, SPEED)
                sleep(SPEED)

            # Get user input from buttons or Bluetooth controller
            i = 0
            while True:
                user_input = False
                while not user_input:
                    if self.wait_to_resume() == 1:
                        GPIO.cleanup()
                        return

                    # Check for button input
                    if GPIO.input(self.buttons[0]) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed(self.leds[0], self.buttons[0])
                        user_input = True
                        pressed_button = self.buttons[0]
                    elif GPIO.input(self.buttons[1]) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed(self.leds[1], self.buttons[1])
                        user_input = True
                        pressed_button = self.buttons[1]
                    elif GPIO.input(self.buttons[2]) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed(self.leds[2], self.buttons[2])
                        user_input = True
                        pressed_button = self.buttons[2]

                    # Check for Bluetooth input if connected
                    if self.client_sock:
                        try:
                            self.client_sock.setblocking(False)
                            data = self.client_sock.recv(1024)
                            if data:
                                received_button = data.decode("utf-8")
                                # print(f"Received button: {received_button}")
                                self.gen_funcs.light_up_led_w_sleep(self.led_dict[received_button], CTLR_LIGHT_UP_SLEEP_TIME)
                                user_input = True
                                pressed_button = self.button_dict[received_button]
                        except BluetoothError as e:
                            if e.errno == 11:
                                pass
                            else:
                                # print(f'Bluetooth disconnected: {e}')
                                self.client_sock.close()
                                self.client_sock = None

                if self.pin_dict[led_sequence[i]] != pressed_button:
                    game_is_playing = False
                    break

                i += 1
                if i == len(led_sequence):
                    break

            sleep(SPEED)
            if game_is_playing:
                self.gen_funcs.flash_all_leds()
                # Change player if playing the multiplayer version
                if self.multiplayer:
                    self.change_player()
                    update_player_callback(self.player)
                update_score_callback(num_round)
            else:
                self.gen_funcs.game_over_flash()
                on_game_over_callback()

            # Attempt to reconnect Bluetooth if disconnected
            if not self.client_sock:
                # print('Rechecking Bluetooth connection...')
                self.client_sock, self.server_sock = self.connect_bluetooth()
            if self.client_sock is None:
                # print("No Bluetooth controller connected. You can continue playing without it.")
                sleep(1)

        # Cleanup
        if self.client_sock:
            self.client_sock.close()
        if self.server_sock:
            self.server_sock.close()
        GPIO.cleanup()

    # Change player number
    def change_player(self):
        self.player = 2 if self.player == 1 else 1

    # Wait to resume if the game is paused
    def wait_to_resume(self):
        while self.pause_event.is_set():
            self.gen_funcs.turn_off_all_leds()
            if self.end_game:
                return 1
            sleep(0.25)
        return 0

    # End game if needed
    def stop(self):
        self.end_game = True
        self.pause_event.set()

    # Pause game by setting pause_event
    def pause(self):
        self.pause_event.set()

    # Resume game by resuming pause_event
    def resume(self):
        self.pause_event.clear()

if __name__ == '__main__':
    memory_game = MemoryGame()
    memory_game.run_game(None, None)
