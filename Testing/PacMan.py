import time
import unicornhathd
from PIL import Image, ImageDraw

def create_pacman_frame(frame):
    img = Image.new('RGB', (16, 16), color='black')
    draw = ImageDraw.Draw(img)

    # Define the mouth angles for different frames
    mouth_angles = {
        1: (30, 330),  # Partially open
        2: (45, 315),  # More open
        3: (60, 300),  # Fully open
    }

    # Draw Pac-Man with varying mouth sizes
    draw.pieslice([(2, 2), (14, 14)], start=mouth_angles[frame][0], end=mouth_angles[frame][1], fill="yellow", outline="black")
    return img

def display_frame(image, offset_x=0):
    width, height = unicornhathd.get_shape()

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel(((x + offset_x) % width, y))
            r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
            unicornhathd.set_pixel(width - 1 + x, y, r, g, b)
    
    unicornhathd.show()

def animate_pacman():
    frames = [create_pacman_frame(i) for i in range(1, 4)]
    width, _ = unicornhathd.get_shape()

    try:
        while True:
            for offset in range(width):
                for frame in frames:
                    display_frame(frame, offset_x=offset)
                    time.sleep(0.1)
    except KeyboardInterrupt:
        unicornhathd.off()

unicornhathd.rotation(270)
unicornhathd.brightness(0.5)

animate_pacman()
