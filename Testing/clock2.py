import unicornhathd
import time
from datetime import datetime

def draw_digit(digit, x_offset, y_offset, brightness=0.5):
    # Patterns for each digit in a 3x5 grid
    patterns = {
        0: [(1,0), (2,0), (0,1), (3,1), (0,2), (3,2), (0,3), (3,3), (1,4), (2,4)],
        1: [(2,0), (1,1), (2,1), (2,2), (2,3), (2,4)],
        2: [(1,0), (2,0), (3,1), (2,2), (1,2), (0,3), (0,4), (1,4), (2,4), (3,4)],
        3: [(1,0), (2,0), (3,1), (2,2), (1,3), (3,3), (1,4), (2,4)],
        4: [(0,1), (3,1), (0,2), (1,2), (2,2), (3,2), (3,3), (3,4)],
        5: [(0,0), (1,0), (2,0), (0,1), (0,2), (1,2), (2,2), (3,3), (1,4), (2,4)],
        6: [(1,0), (2,0), (0,1), (0,2), (1,2), (2,2), (0,3), (3,3), (1,4), (2,4)],
        7: [(0,0), (1,0), (2,0), (3,0), (3,1), (2,2), (2,3), (2,4)],
        8: [(1,0), (2,0), (0,1), (3,1), (1,2), (2,2), (0,3), (3,3), (1,4), (2,4)],
        9: [(1,0), (2,0), (0,1), (3,1), (1,2), (2,2), (3,2), (3,3), (1,4), (2,4)]
    }

 
def clear_digit(x_offset, y_offset):
    for x in range(3):
        for y in range(5):
            unicornhathd.set_pixel(x + x_offset, y + y_offset, 0, 0, 0)

# Initialize the display
unicornhathd.rotation(0)
unicornhathd.brightness(0.5)

while True:
    now = datetime.now()
    hour = now.hour
    minute = now.minute

    # Split the hour and minute into single digits
    hour_tens = hour // 10
    hour_ones = hour % 10
    minute_tens = minute // 10
    minute_ones = minute % 10

    # Clear the display
    unicornhathd.clear()

    # Draw each digit
    draw_digit(hour_tens, 0, 0)
    draw_digit(hour_ones, 4, 0)
    draw_digit(minute_tens, 9, 0)
    draw_digit(minute_ones, 13, 0)

    # Update the display
    unicornhathd.show()

    # Wait for a minute before updating
    time.sleep(60)
