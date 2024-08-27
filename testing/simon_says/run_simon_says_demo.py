import sys
import simon_says_demo
import RPi.GPIO as GPIO
import threading
from time import sleep

global THREAD_FLAG
THREAD_FLAG = False

# Start button: GPIO 10
start_button = 10

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(start_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def stop_demo():
    global THREAD_FLAG
    THREAD_FLAG = True
    simon_says_demo.stop()

if __name__ == "__main__":
    try:
        init_gpio()
        demo_thread = threading.Thread()
        while True:
            init_gpio()
            if GPIO.input(start_button) == GPIO.LOW:
                if demo_thread.is_alive():
                    print("STOP REQUEST")
                    stop_demo()
                    demo_thread.join()
                    sleep(0.5)
                else:
                    THREAD_FLAG = False
                    demo_thread = threading.Thread(target=simon_says_demo.main)
                    demo_thread.start()
                    sleep(0.5)
                    init_gpio()
            sleep(0.15)
    except KeyboardInterrupt:
        stop_demo()
        GPIO.cleanup()
