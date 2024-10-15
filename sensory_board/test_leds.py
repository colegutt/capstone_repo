###LED_Shapes.py###
# Imports for required libraries
import time
import board
import neopixel

# Set up neopixels
pixel_pin = board.D18
num_leds = 40

pixels = neopixel.NeoPixel(pixel_pin, num_leds)

# Create an array object the size of your led strip
np_array = list(range(num_leds+1))

# Create slice objects corresponding to the LED indices for each area
#   and give those ranges of your LED strand meaningful names
star_slice = slice(0, 5)
star = np_array[star_slice]

circle_slice = slice(5,10)
circle = np_array[circle_slice]

heart_slice = slice(10, 15)
heart = np_array[heart_slice]

triangle_slice = slice(15,20)
triangle = np_array[triangle_slice]

cloud_slice = slice(20, 25)
cloud = np_array[cloud_slice]

square_slice = slice(25,30)
square = np_array[square_slice]

def turn_on_all_leds():
    # Assign the same value to every LED in the named range
    # Turn on all sections
    for p in star:
        pixels[p] = (255, 165, 0)  # Yellow
    for p in circle:
        pixels[p] = (255, 100, 0)  # Orange
    for p in heart:
        pixels[p] = (255, 0, 0)    # Red
    for p in triangle:
        pixels[p] = (128, 0, 128)  # Purple
    for p in cloud:
        pixels[p] = (0, 0, 255)    # Blue
    for p in square:
        pixels[p] = (0, 255, 0)    # Green

    pixels.show()

def turn_on_square():
    for p in square:
        pixels[p] = (0, 255, 0)    # Green

    pixels.show()


def turn_off_leds():
    # Turn off all sections
    for p in star:
        pixels[p] = (0, 0, 0)  # Turn off (black)
    for p in circle:
        pixels[p] = (0, 0, 0)  # Turn off (black)
    for p in heart:
        pixels[p] = (0, 0, 0)  # Turn off (black)
    for p in triangle:
        pixels[p] = (0, 0, 0)  # Turn off (black)
    for p in cloud:
        pixels[p] = (0, 0, 0)  # Turn off (black)
    for p in square:
        pixels[p] = (0, 0, 0)  # Turn off (black)

    pixels.show()


# turn_on_all_leds()
# turn_on_square()
turn_off_leds()