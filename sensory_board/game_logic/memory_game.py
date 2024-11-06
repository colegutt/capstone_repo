import RPi.GPIO as GPIO
from time import sleep
import random
import threading
from general_functions import GeneralFunctions
from bluetooth import BluetoothSocket, BluetoothError, RFCOMM

# Game Parameters
SPEED = 0.5
CTLR_LIGHT_UP_SLEEP_TIME = 0.25
CLIENT_SOCK_SLEEP_TIME = 0.25

class MemoryGame:
    def __init__(self, app_init, multiplayer=False, player_count=1, game_mode='Cooperative'):
        # Initializations
        self.pause_event = threading.Event()
        self.gen_funcs = GeneralFunctions(app_init=app_init)
        self.end_game = False

        # Multiplayer parameters
        self.player = 1
        self.multiplayer = multiplayer
        self.player_count = player_count
        self.player_arr = self.get_player_arr()
        self.elimination = False
        if game_mode == 'Elimination':
            self.elimination = True

        # self.pin_dict, self.buttons, self.leds = self.gen_funcs.init_gpio()
        self.button_dict, self.led_shapes = self.gen_funcs.init_leds_and_buttons()
        self.gen_funcs.turn_off_all_leds()

        # Bluetooth initialization
        self.client_sock, self.server_sock = self.connect_bluetooth()

    def connect_bluetooth(self):
        # print('Checking for Bluetooth controller...')
        port = 1
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
                sleep(CLIENT_SOCK_SLEEP_TIME)  # Retry every 1 second
            return None, server_sock

        # Start checking for connection in a separate thread
        connection_thread = threading.Thread(target=attempt_accept, daemon=True)
        connection_thread.start()

        return None, server_sock  # Return None for client_sock until connection is made

    # Function to disconnect the Bluetooth client
    def disconnect_bluetooth(self):
        if self.client_sock:
            try:
                self.client_sock.close()
            except BluetoothError as e:
                print(f"Error disconnecting Bluetooth: {e}")
            finally:
                self.client_sock = None
        if self.server_sock:
            try:
                self.server_sock.close()
            except BluetoothError as e:
                print(f"Error closing Bluetooth server socket: {e}")
            finally:
                self.server_sock = None

    # Start memory game
    def run_game(self, update_score_callback, on_game_over_callback, update_player_callback=None):
        game_is_playing = True
        num_round = 0
        led_sequence = []
        repeat_sequence = False

        while game_is_playing:
            # Light up LED sequence
            if not repeat_sequence:
                num_round += 1
                led_sequence.append(random.choice(self.led_shapes)) 
                for led_shape in led_sequence:
                    if self.wait_to_resume() == 1:
                        GPIO.cleanup()
                        return
                    self.gen_funcs.light_up_led_w_sleep(led_shape, SPEED)
                    sleep(SPEED)

            # Get user input from buttons or Bluetooth controller
            i = 0
            while True:
                user_input = False
                pressed_button = None
                while not user_input:
                    if self.wait_to_resume() == 1:
                        GPIO.cleanup()
                        return

                    # Check for button input
                    if GPIO.input(self.button_dict['square']) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed('square', self.button_dict['square'])
                        user_input = True
                        pressed_button = self.button_dict['square']
                    elif GPIO.input(self.button_dict['triangle']) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed('triangle', self.button_dict['triangle'])
                        user_input = True
                        pressed_button = self.button_dict['triangle']
                    elif GPIO.input(self.button_dict['circle']) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed('circle', self.button_dict['circle'])
                        user_input = True
                        pressed_button = self.button_dict['circle']
                    elif GPIO.input(self.button_dict['cloud']) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed('cloud', self.button_dict['cloud'])
                        user_input = True
                        pressed_button = self.button_dict['cloud']
                    elif GPIO.input(self.button_dict['heart']) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed('heart', self.button_dict['heart'])
                        user_input = True
                        pressed_button = self.button_dict['heart']
                    elif GPIO.input(self.button_dict['star']) == GPIO.LOW:
                        self.gen_funcs.light_up_led_as_long_as_pressed('star', self.button_dict['star'])
                        user_input = True
                        pressed_button = self.button_dict['star']

                    # Check for Bluetooth input if connected
                    if pressed_button == None:
                        user_input, pressed_button = self.check_for_controller_input(user_input)
                    
                    sleep(0.1)

                if self.button_dict[led_sequence[i]] != pressed_button:
                    game_is_playing = False
                    break

                i += 1
                if i == len(led_sequence):
                    break

            sleep(SPEED)
            if game_is_playing:
                if repeat_sequence:
                    repeat_sequence = False
                self.gen_funcs.memory_correct_sequence_flash()
                # Change player if playing the multiplayer version
                if self.multiplayer:
                    if self.elimination and len(self.player_arr) == 1:
                        self.gen_funcs.game_over_flash()
                        game_is_playing = False
                        on_game_over_callback(self.player)
                    else:
                        self.change_player()
                        update_player_callback(self.player)
                update_score_callback(num_round)
            else:
                if self.elimination and len(self.player_arr) > 1:
                    eliminated_player = self.player
                    self.change_player()
                    self.player_arr.remove(eliminated_player)
                    update_player_callback(eliminated_player, True)
                    self.gen_funcs.fast_tap_wrong_led()
                    sleep(1)
                    game_is_playing = True
                    update_player_callback(self.player)
                    repeat_sequence = True
                else:
                    if self.elimination:
                        self.gen_funcs.fast_tap_wrong_led()
                    self.gen_funcs.game_over_flash()
                    on_game_over_callback()

            # Attempt to reconnect Bluetooth if disconnected
            if not self.client_sock:
                # print('Rechecking Bluetooth connection...')
                self.client_sock, self.server_sock = self.connect_bluetooth()
            if self.client_sock is None:
                # print("No Bluetooth controller connected. You can continue playing without it.")
                sleep(CLIENT_SOCK_SLEEP_TIME)

        # Cleanup
        if self.client_sock:
            self.client_sock.close()
        if self.server_sock:
            self.server_sock.close()
        
        GPIO.cleanup()

    # Change player number
    def change_player(self):
        current_index = self.player_arr.index(self.player)
        next_index = (current_index + 1) % len(self.player_arr)
        self.player = self.player_arr[next_index]
    
    def get_player_arr(self):
        player_arr = []
        all_players_arr = [
            1, 2, 3, 4, 5, 6, 7, 8
        ]
        for i in range(0, self.player_count):
            player_arr.append(all_players_arr[i])
        return player_arr
    
    def check_for_controller_input(self, user_input):
        pressed_button = None
        if self.client_sock:
            try:
                self.client_sock.setblocking(False)
                data = self.client_sock.recv(1024)
                if data:
                    received_button_shape = data.decode("utf-8")
                    # print(f"Received button: {received_button}")
                    self.gen_funcs.light_up_led_w_sleep(received_button_shape, CTLR_LIGHT_UP_SLEEP_TIME)
                    user_input = True
                    pressed_button = self.button_dict[received_button_shape]
            except BluetoothError as e:
                if e.errno == 11:
                    pass
                else:
                    # print(f'Bluetooth disconnected: {e}')
                    self.client_sock.close()
                    self.client_sock = None
        return user_input, pressed_button
        

    # Wait to resume if the game is paused
    def wait_to_resume(self):
        if self.pause_event.is_set():
            self.gen_funcs.turn_off_all_leds()
        while self.pause_event.is_set():
            if self.end_game:
                return 1
            sleep(0.25)
        return 0

    # End game if needed
    def stop(self):
        self.end_game = True
        self.disconnect_bluetooth()
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
