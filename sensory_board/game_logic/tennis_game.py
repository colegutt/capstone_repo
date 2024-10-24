import RPi.GPIO as GPIO
from time import sleep, time
import threading
from general_functions import GeneralFunctions
from bluetooth import BluetoothSocket, BluetoothError, RFCOMM

CLIENT_SOCK_SLEEP_TIME = 0.25
STARTING_SPEED = 1

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
        self.thread_flag_1 = False
        self.thread_flag_2 = False

        self.sleep_time = STARTING_SPEED

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
        triangle_flashing = threading.Thread(target=self.flash_led)
        triangle_flashing.start()

        while GPIO.input(self.button_dict['triangle']) == GPIO.HIGH:
            sleep(0.1)

        self.gen_funcs.turn_off_led('triangle')
        self.thread_flag_1 = True

        while True:
            if not self.light_up_over_net('cw'):
                break
        
            if not self.wait_for_return('square'):
                break
        
            if not self.light_up_over_net('ccw'):
                break

            if not self.wait_for_return('triangle'):
                break

        self.gen_funcs.fast_tap_wrong_led()
        
        sleep(self.sleep_time)
        
        GPIO.cleanup()

    def wait_for_return(self, led_shape):
        print('lighting up led')
        self.gen_funcs.light_up_led(led_shape)
        start_time = time()
        success = False
        while time() - start_time < self.sleep_time:
            if GPIO.input(self.button_dict[led_shape]) == GPIO.LOW:
                success = True
                break
        self.gen_funcs.turn_off_led(led_shape)
        return success

    def monitor_button_press(self, button_pressed_event, shape_traveling_to):
        while not button_pressed_event.is_set():
            if GPIO.input(self.button_dict[shape_traveling_to]) == GPIO.LOW:
                button_pressed_event.set()  # Signal that the button has been pressed
                break
            elif self.thread_flag_2:
                break

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
            
            self.gen_funcs.turn_off_led(led_shape) 

        self.thread_flag_2 = True
        return success


    def flash_led(self):
        while not self.thread_flag_1 == True:
            self.gen_funcs.light_up_led('triangle', False)
            sleep(0.5)
            self.gen_funcs.turn_off_led('triangle')
            sleep(0.5)

    def stop(self):
        self.end_game = True
        self.disconnect_bluetooth()
        self.pause_event.set()

    def pause(self):
        self.pause_event.set
