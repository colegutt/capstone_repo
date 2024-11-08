###LED_Shapes.py###
# Imports for required libraries
import time
import board
import neopixel

# Set up neopixels
pixel_pin = board.D18
num_leds = 40

#Putting up a Global Brightness control 
pixels = neopixel.NeoPixel(pixel_pin, num_leds)#, brightness = 0.5) #Starts LED at 50% brightness

#Function to dim LEDs, this is a manual dimming. Pretty sure this is the way we want to go with the dimming.
def dim_color(color, factor):
    """Dim the RGB color by the given factor (0.0 to 1.0)"""
    return tuple(int(c*factor)for c in color)

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

def turn_on_all_leds(dimming_factor):
    for p in star:
        pixels[p] = dim_color((0, 0, 255), dimming_factor)   # Dimmable Yellow
    for p in circle:
        pixels[p] = dim_color((255, 100, 0), dimming_factor)  # Dimmable Orange
    for p in heart:
        pixels[p] = dim_color((128, 0, 128), dimming_factor)    # Dimmable Red
    for p in triangle:
        pixels[p] = dim_color((128, 0, 128), dimming_factor)  # Dimmable Purple
    for p in cloud:
        pixels[p] = dim_color((0, 255, 0), dimming_factor)    # Dimmable Blue
    for p in square:
        pixels[p] = dim_color((0, 255, 0), dimming_factor)    # Dimmable Green

    pixels.show()

def turn_on_test_strip(dimming_factor, color):
    for p in star:
        pixels[p] = dim_color(color, dimming_factor) 

def test_led_main(color):
    try:
        while True:
            turn_off_leds()
            turn_on_test_strip(0.1, color)
            time.sleep(1)
            turn_off_leds()
            turn_on_test_strip(0.25, color)
            time.sleep(1)
            turn_off_leds()
            turn_on_test_strip(0.5, color)
            time.sleep(1)
            turn_off_leds()
            turn_on_test_strip(0.75, color)
            time.sleep(1)
            turn_off_leds()
            turn_on_test_strip(1, color)
            time.sleep(1)
            turn_off_leds()
    except KeyboardInterrupt:
        turn_off_leds()

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

green_square_color = (0, 255, 0)
blue_cloud_color = (0, 0, 255)
purple_triangle_color = (128, 0, 128)
red_heart_color = (255, 0, 0)
orange_circle_color = (255, 100, 0)
yellow_star_color = (255, 165, 0)

test_led_main(green_square_color)