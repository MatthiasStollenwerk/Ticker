import time
import unicornhathd
from PIL import Image, ImageDraw

def create_pacman_frame(frame):
    img = Image.new('RGB', (16, 16), color='white')
    draw = ImageDraw.Draw(img)

    # Define the mouth angles for different frames
    mouth_angles = {
        1: (190, 170),  # Partially open
        2: (225, 135),  # More open
        3: (240, 120),  # Fully open
    }

    # Draw Pac-Man with varying mouth sizes
    draw.pieslice([(2, 2), (14, 14)], start=mouth_angles[frame][0], end=mouth_angles[frame][1], fill="blue", outline="black")
    return img

def display_frame(image, offset_x=0):
    width, height = unicornhathd.get_shape()

    for x in range(width):
        for y in range(height):
            # Calculate the correct pixel position
            pixel_position = (x + offset_x) % (width + image.width)
            if pixel_position < width:
                pixel = image.getpixel((pixel_position, y))
                r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                unicornhathd.set_pixel(x, y, r, g, b)
            else:
                unicornhathd.set_pixel(x, y, 255, 255, 255)
    
    unicornhathd.show()

def animate_pacman():
    frames = [create_pacman_frame(i) for i in range(1, 4)]
    width, _ = unicornhathd.get_shape()

    for offset in range(-width, width):
        for frame in frames:
            display_frame(frame, offset_x=offset)
            time.sleep(0.05)

unicornhathd.rotation(270)
unicornhathd.brightness(0.5)

try:
    while True:
        animate_pacman()
except KeyboardInterrupt:
        unicornhathd.off()