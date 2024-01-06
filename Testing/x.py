import unicornhathd
import random
import time

# Set the brightness of the LEDs
unicornhathd.brightness(0.5)

def generate_pixel_art():
    while True:
        for y in range(16):
            for x in range(16):
                # Generate random colors
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                unicornhathd.set_pixel(x, y, r, g, b)
        
        unicornhathd.show()
        time.sleep(0.5)

try:
    generate_pixel_art()
except KeyboardInterrupt:
    unicornhathd.off()
