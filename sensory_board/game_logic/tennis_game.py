import RPi.GPIO as GPIO
import random
from time import sleep, time
import threading
from general_functions import GeneralFunctions
from bluetooth import BluetoothSocket, BluetoothError, RFCOMM
from PyQt5.QtCore import pyqtSignal

CLIENT_SOCK_SLEEP_TIME = 0.25
STARTING_SPEED = 0.75
SPEED_ACCELERATION = 0.75
POINTS_PLAYED_TO = 3

class TennisGame:
    def __init__(self, app_init):
        self.pause_event = threading.Event()
        self.app_init = app_init
        self.gen_funcs = GeneralFunctions(app_init=app_init)
        self.end_game = False
        self.start_time = None
        self.button_dict, self.led_shapes = self.gen_funcs.init_leds_and_buttons()
        self.gen_funcs.turn_off_all_leds()
        # self.client_sock, self.server_sock = self.connect_bluetooth()
        self.thread_flag = None
        self.player_1_score = 0
        self.player_2_score = 0
        self.player1_score_updated = pyqtSignal(int)
        self.player2_score_updated = pyqtSignal(int)
        self.rally_updated = pyqtSignal(int)
        self.serving_player = 1

        self.sleep_time = STARTING_SPEED

    def run_game(self, update_score_callback, update_rally_callback, on_game_over_callback):
        try:
            while True:
                if self.serving_player == 1:
                    if self.play_round('triangle', 'cw', 'ccw', 'square', update_score_callback, update_rally_callback) == 1:
                        return
                elif self.serving_player == 2:
                    if self.play_round('square', 'ccw', 'cw', 'triangle', update_score_callback, update_rally_callback) == 1:
                        return

                self.sleep_time = STARTING_SPEED
                self.serving_player = 1 if self.serving_player == 2 else 2

                if self.player_1_score == POINTS_PLAYED_TO:
                    self.gen_funcs.game_over_flash()
                    on_game_over_callback(1)
                    break
                elif self.player_2_score == POINTS_PLAYED_TO:
                    self.gen_funcs.game_over_flash()
                    on_game_over_callback(2)
                    break
                
                sleep(0.5)
            
            self.pause_event.clear()
            del self.pause_event
            GPIO.cleanup()
        except:
            self.stacked_widget.setCurrentIndex(20)
    
    def play_round(self, shape_1, dir_1, dir_2, shape_2, update_score_callback, update_rally_callback):
        self.app_init.tennis_ingame_screen.toggle_pause_button(True)
        self.thread_flag = 'off'
        server_button_flashing = threading.Thread(target=self.flash_led, args=(shape_1,))
        server_button_flashing.start()

        # Wait to serve
        while GPIO.input(self.button_dict[shape_1]) == GPIO.HIGH:
            if self.wait_to_resume(shape_1) == 1:
                self.pause_event.clear()
                del self.pause_event
                GPIO.cleanup()
                return 1
            # if self.check_for_controller_input(shape_1):
            #     break
            sleep(0.1)

        self.gen_funcs.turn_off_led(shape_1)
        self.thread_flag = 'on'

        server_button_flashing.join()

        self.app_init.tennis_ingame_screen.toggle_pause_button(False)

        rally = 1

        while True:
            update_rally_callback(rally)
            if not self.light_up_over_net(dir_1):
                self.determine_who_scores(dir=dir_1, update_score_callback=update_score_callback)
                break
            
            if not self.wait_for_return(shape_2):
                self.determine_who_scores(shape=shape_2, update_score_callback=update_score_callback)
                break

            rally += 1
            self.increase_ball_speed(rally)
            update_rally_callback(rally)

            if not self.light_up_over_net(dir_2):
                self.determine_who_scores(dir=dir_2, update_score_callback=update_score_callback)
                break

            if not self.wait_for_return(shape_1):
                self.determine_who_scores(shape=shape_1, update_score_callback=update_score_callback)
                break
                
            rally += 1
            self.increase_ball_speed(rally)
        
        self.save_high_score(rally)
        self.gen_funcs.fast_tap_wrong_led()

    def increase_ball_speed(self, rally):
        if rally > 15:
            if self.sleep_time <= 0.0001:
                self.sleep_time = 0.0001
            else:
                self.sleep_time *= SPEED_ACCELERATION * 0.75
        else:
            decision = random.randint(1, 7)
            if decision == 1:
                # Slow down (14%)
                self.sleep_time *= (SPEED_ACCELERATION * 1.5)
            elif decision == 2 or decision == 3:
                # Speed up (29%)
                self.sleep_time *= SPEED_ACCELERATION
            elif decision == 4 or decision == 5:
                # Speed up faster (29%)
                self.sleep_time *= (SPEED_ACCELERATION / 1.5)
            # Do nothing (29%)

    def save_high_score(self, rally):
        if self.app_init.tennis_hs < rally:
            self.app_init.tennis_hs = rally
            self.app_init.mp_screen.update_displayed_values()
            self.app_init.save_tennis_high_score()

    def determine_who_scores(self, dir=None, shape=None, update_score_callback=None):
        if dir == 'cw':
            self.player_1_score += 1
            update_score_callback(1, self.player_1_score)
        elif dir == 'ccw':
            self.player_2_score += 1
            update_score_callback(2, self.player_2_score)
        elif shape == 'triangle':
            self.player_2_score += 1
            update_score_callback(2, self.player_2_score)
        elif shape == 'square':
            self.player_1_score += 1
            update_score_callback(1, self.player_1_score)

    def wait_for_return(self, led_shape):
        self.gen_funcs.light_up_led(led_shape)
        start_time = time()
        success = False
        while time() - start_time < self.sleep_time:
            if GPIO.input(self.button_dict[led_shape]) == GPIO.LOW:
                success = True
                break
        self.gen_funcs.turn_off_led(led_shape)
        return success

    def light_up_over_net(self, cw_or_ccw):
        success = True

        if cw_or_ccw == 'cw':
            led_shapes = ['heart', 'circle', 'star']
            shape_traveling_to = 'square'
        else:
            led_shapes = ['star', 'circle', 'heart']
            shape_traveling_to = 'triangle'

        for led_shape in led_shapes:
            self.gen_funcs.light_up_led(led_shape)

            start_time = time()
            while time() - start_time < self.sleep_time:
                if GPIO.input(self.button_dict[shape_traveling_to]) == GPIO.LOW:
                    self.gen_funcs.turn_off_led(led_shape)
                    return False
                sleep(0.1)
            self.gen_funcs.turn_off_led(led_shape) 
        return success

    def flash_led(self, led_shape):
        while self.thread_flag == 'off' or self.thread_flag == 'pause':
            while self.thread_flag == 'pause':
                sleep(0.1)
            self.gen_funcs.light_up_led(led_shape)
            sleep(0.5)
            self.gen_funcs.turn_off_led(led_shape)
            sleep(0.5)

    def stop(self):
        self.end_game = True
        # self.disconnect_bluetooth()

    def pause(self):
        self.pause_event.set()

    def wait_to_resume(self, shape_1):
        if self.pause_event.is_set():
            self.gen_funcs.turn_off_all_leds()
            self.thread_flag = 'pause'
        while self.pause_event.is_set():
            if self.end_game:
                return 1
            sleep(0.25)
        self.thread_flag = 'off'
        return 0
        
    def resume(self):
        self.pause_event.clear()