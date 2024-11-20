import RPi.GPIO as GPIO
from time import sleep, time
import random
import threading
from general_functions import GeneralFunctions
from bluetooth import BluetoothSocket, BluetoothError, RFCOMM

# Game Parameters
GAME_RUN_TIME = 30
SPEED = 0.20  # This is the lowest number we can do
CTLR_LIGHT_UP_SLEEP_TIME = 0.25
CLIENT_SOCK_SLEEP_TIME = 0.25

class FastTapGame:
    def __init__(self, stacked_widget, app_init):
        # Create pause event
        self.pause_event = threading.Event()
        self.stacked_widget = stacked_widget

        # Set parameters that control the game
        self.gen_funcs = GeneralFunctions(app_init=app_init)
        self.end_game = False
        self.time_remaining = GAME_RUN_TIME
        self.start_time = None

        # Intialize GPIO pins
        self.button_dict, self.led_shapes = self.gen_funcs.init_leds_and_buttons()

        # All games turn off LEDs to start
        self.gen_funcs.turn_off_all_leds()

        # Bluetooth initialization
        self.client_sock, self.server_sock = self.connect_bluetooth()

    def connect_bluetooth(self):
        port = 1
        server_sock = BluetoothSocket(RFCOMM)

        try:
            server_sock.bind(("", port))
            server_sock.listen(1)
            server_sock.setblocking(False)  # Set non-blocking mode
        except BluetoothError as e:
            return None, server_sock

        # Function to periodically check for Bluetooth connection
        def attempt_accept():
            client_sock = None
            while client_sock is None:
                try:
                    client_sock, client_info = server_sock.accept()
                    self.client_sock = client_sock
                    return client_sock, server_sock
                except BluetoothError as e:
                    if e.errno == 11:  # No connection yet (non-blocking)
                        sleep(0.01)
                    else:
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

    # Function that runs the fast tap game
    def run_game(self, update_score_callback, update_timer_callback, on_game_over_callback):
        try:
            score = 0
            self.start_time = time()
            while not self.end_game and self.time_remaining > 0:
                # Light up a random LED
                current_led_shape = random.choice(self.led_shapes)
                self.gen_funcs.light_up_led(current_led_shape)
                user_input = False
                while not user_input:
                    self.update_time()

                    if self.time_remaining  == 0:
                        break

                    # Pause Condition
                    resume_opt = self.wait_to_resume()
                    if resume_opt == 'end':
                        GPIO.cleanup()
                        return
                    elif resume_opt == 'resume':
                        break

                    # Check for button input
                    if self.gen_funcs.detect_button_press(self.button_dict[current_led_shape]) and all(GPIO.input(self.button_dict[led_shape]) == GPIO.HIGH for led_shape in self.led_shapes if led_shape != current_led_shape):
                        # Correct button is pressed
                        user_input = True
                        self.gen_funcs.turn_off_all_leds()
                        score += 1
                        update_score_callback(score)

                    elif any(self.gen_funcs.detect_button_press(self.button_dict[led_shape]) for led_shape in self.led_shapes if led_shape != current_led_shape):
                        # A wrong button is pressed
                        user_input = True
                        self.gen_funcs.fast_tap_wrong_led()

                    # Check for Bluetooth input if connected
                    if not user_input:
                        user_input, score = self.check_for_controller_input(user_input, current_led_shape, update_score_callback, score)

                self.update_time()
                update_timer_callback(self.time_remaining)

                # Pause for next LED to light up
                sleep(SPEED)

            self.gen_funcs.game_over_flash()
            on_game_over_callback()
            self.pause_event.clear()
            GPIO.cleanup()
        except Exception as e:
            print(e)
            self.stacked_widget.setCurrentIndex(20)

    # Update time using the time that has passed
    def update_time(self):
        elapsed_time = time() - self.start_time
        self.time_remaining = GAME_RUN_TIME - int(elapsed_time)
    
    def check_for_controller_input(self, user_input, current_led_shape, update_score_callback, score):
        if self.client_sock:
            if user_input:
                return user_input
            try:
                self.client_sock.setblocking(False)
                data = self.client_sock.recv(1024)
                if data:
                    received_button = data.decode("utf-8")
                    if current_led_shape == received_button:
                        user_input = True
                        self.gen_funcs.turn_off_all_leds()
                        score += 1
                        update_score_callback(score)
                    else:
                        user_input = True
                        self.gen_funcs.fast_tap_wrong_led()
            except BluetoothError as e:
                if e.errno == 11:
                    pass
                else:
                    self.client_sock.close()
                    self.client_sock = None
        return user_input, score

    # Function that pauses the game while in the pause screen
    def wait_to_resume(self):
        resume_opt = None
        if self.pause_event.is_set():
            self.gen_funcs.turn_off_all_leds()

        while self.pause_event.is_set():
            resume_opt = 'resume'
            if self.end_game:
                self.pause_event.clear()
                return 'end'
            sleep(0.1)
        
        if resume_opt == 'resume':
            self.start_time = time()
        return resume_opt

    # End the game
    def stop(self):
        self.end_game = True
        self.disconnect_bluetooth()

    # Pause the game by setting the pause event
    def pause(self):
        self.pause_event.set()

    # Resume the game by clearing the pause event
    def resume(self):
        self.pause_event.clear()

# Main function if we want to run the game independently
if __name__ == '__main__':
    fast_tap_game = FastTapGame()
    fast_tap_game.run_game(None, None, None)
