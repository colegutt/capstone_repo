import RPi.GPIO as GPIO
from time import sleep, time
import threading
from general_functions import GeneralFunctions
from bluetooth import BluetoothSocket, BluetoothError, RFCOMM

CLIENT_SOCK_SLEEP_TIME = 0.25
STARTING_SPEED = 1
SPEED_ACCELERATION = 0.75

class TennisGame:
    def __init__(self, app_init):
        self.pause_event = threading.Event()
        self.app_init = app_init
        self.gen_funcs = GeneralFunctions(app_init=app_init)
        self.end_game = False
        self.start_time = None
        self.button_dict, self.led_shapes = self.gen_funcs.init_leds_and_buttons()
        self.gen_funcs.turn_off_all_leds()
        self.client_sock, self.server_sock = self.connect_bluetooth()
        self.thread_flag_1 = None
        self.thread_flag_2 = False
        self.player_1_score = 0
        self.player_2_score = 0
        self.serving_player = 1

        self.sleep_time = STARTING_SPEED
        # Initialize variables to control the pause button visibility
        self.on_wait_for_serve = True

    def connect_bluetooth(self):
        port = 1
        server_sock = BluetoothSocket(RFCOMM)
        try:
            server_sock.bind(("", port))
            server_sock.listen(1)
            server_sock.setblocking(False)
        except BluetoothError as e:
            return None, server_sock

        def attempt_accept():
            client_sock = None
            while client_sock is None:
                try:
                    client_sock, client_info = server_sock.accept()
                    self.client_sock = client_sock
                    return client_sock, server_sock
                except BluetoothError as e:
                    if e.errno == 11:
                        sleep(0.01)
                    else:
                        break
                sleep(CLIENT_SOCK_SLEEP_TIME)
            return None, server_sock

        connection_thread = threading.Thread(target=attempt_accept, daemon=True)
        connection_thread.start()

        return None, server_sock

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

    def run_game(self):
        while True:
            print('starting round')
            if self.serving_player == 1:
                if self.play_round('triangle', 'cw', 'ccw', 'square') == 1:
                    return
            elif self.serving_player == 2:
                if self.play_round('square', 'ccw', 'cw', 'triangle') == 1:
                    return

            self.sleep_time = STARTING_SPEED
            self.serving_player = 1 if self.serving_player == 2 else 2

            print(f'PLAYER 1 SCORE: {self.player_1_score}')
            print(f'PLAYER 2 SCORE: {self.player_2_score}')
            if self.player_1_score == 5:
                print('PLAYER 1 WINS! GAME OVER!')
                break
            elif self.player_2_score == 3:
                print('PLAYER 2 WINS! GAME OVER!')
                break
            
            sleep(1)
            
        GPIO.cleanup()
    
    def play_round(self, shape_1, dir_1, dir_2, shape_2):
        # Signal that we are waiting for a serve (pause button visible)
        self.on_wait_for_serve = True
        self.app_init.tennis_ingame_screen.toggle_pause_button(True)

        self.thread_flag_1 = 'off'
        server_button_flashing = threading.Thread(target=self.flash_led, args=(shape_1,))
        server_button_flashing.start()

        while GPIO.input(self.button_dict[shape_1]) == GPIO.HIGH:
            if self.wait_to_resume(shape_1) == 1:
                GPIO.cleanup()
                return 1
            if self.check_for_controller_input(shape_1):
                break
            sleep(0.1)

        self.gen_funcs.turn_off_led(shape_1)
        self.thread_flag_1 = 'on'

        self.on_wait_for_serve = False
        self.app_init.tennis_ingame_screen.toggle_pause_button(False)

        while True:
            if not self.light_up_over_net(dir_1):
                self.determine_who_scores(dir=dir_1)
                break
        
            if not self.wait_for_return(shape_2):
                self.determine_who_scores(shape=shape_2)
                break
        
            if not self.light_up_over_net(dir_2):
                self.determine_who_scores(dir=dir_2)
                break

            if not self.wait_for_return(shape_1):
                self.determine_who_scores(shape=shape_1)
                break

            self.sleep_time = self.sleep_time * SPEED_ACCELERATION
        
        self.gen_funcs.fast_tap_wrong_led()

        # Signal end of round (waiting for next serve)
        self.on_wait_for_serve = True

    def determine_who_scores(self, dir=None, shape=None):
        print('determining who scored')
        if dir == 'cw':
            self.player_1_score += 1
        elif dir == 'ccw':
            self.player_2_score += 1
        elif shape == 'triangle':
            self.player_2_score += 1
        elif shape == 'square':
            self.player_1_score += 1

    def wait_for_return(self, led_shape):
        self.gen_funcs.light_up_led(led_shape)
        start_time = time()
        success = False
        while time() - start_time < self.sleep_time:
            if GPIO.input(self.button_dict[led_shape]) == GPIO.LOW:
                success = True
                break
            if self.check_for_controller_input(led_shape):
                success = True
                break
        self.gen_funcs.turn_off_led(led_shape)
        return success
    
    def check_for_controller_input(self, led_shape):
        button_pressed = False
        if self.client_sock:
            try:
                self.client_sock.setblocking(False)
                data = self.client_sock.recv(1024)
                if data:
                    received_button_shape = data.decode("utf-8")
                    if received_button_shape == led_shape:
                        button_pressed = True
            except BluetoothError as e:
                if e.errno == 11:
                    pass
                else:
                    self.client_sock.close()
                    self.client_sock = None
        return button_pressed

    def monitor_button_press(self, button_pressed_event, shape_traveling_to):
        while not button_pressed_event.is_set():
            if GPIO.input(self.button_dict[shape_traveling_to]) == GPIO.LOW:
                button_pressed_event.set()
                break
            elif self.check_for_controller_input(shape_traveling_to):
                button_pressed_event.set()
                break
            elif self.thread_flag_2:
                return

    def light_up_over_net(self, cw_or_ccw):
        success = True
        button_pressed_event = threading.Event()  # Event to signal button press

        if cw_or_ccw == 'cw':
            led_shapes = ['heart', 'circle', 'star']
            shape_traveling_to = 'square'
        else:
            led_shapes = ['star', 'circle', 'heart']
            shape_traveling_to = 'triangle'

        self.thread_flag_2 = False
        monitoring_thread = threading.Thread(target=self.monitor_button_press, args=(button_pressed_event, shape_traveling_to))
        monitoring_thread.start()

        for led_shape in led_shapes:
            self.gen_funcs.light_up_led(led_shape)

            start_time = time()
            while time() - start_time < self.sleep_time:
                if button_pressed_event.is_set(): 
                    success = False
                    self.gen_funcs.turn_off_led(led_shape)
                    monitoring_thread.join()
                    self.thread_flag_2 = True
                    return success
                sleep(0.1)
            
            self.gen_funcs.turn_off_led(led_shape) 

        self.thread_flag_2 = True
        return success

    def flash_led(self, led_shape):

        while self.thread_flag_1 == 'off' or self.thread_flag_1 == 'pause':
            while self.thread_flag_1 == 'pause':
                sleep(0.1)
            self.gen_funcs.light_up_led(led_shape, False)
            sleep(0.5)
            self.gen_funcs.turn_off_led(led_shape)
            sleep(0.5)

    def stop(self):
        self.end_game = True
        self.disconnect_bluetooth()
        self.pause_event.set()

    def pause(self):
        self.pause_event.set()

    def wait_to_resume(self, shape_1):
        if self.pause_event.is_set():
            self.gen_funcs.turn_off_all_leds()
            self.thread_flag_1 = 'pause'
        while self.pause_event.is_set():
            if self.end_game:
                return 1
            sleep(0.25)
        self.thread_flag_1 = 'off'
        return 0
        
    def resume(self):
        self.pause_event.clear()