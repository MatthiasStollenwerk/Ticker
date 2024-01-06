import time
import unicornhathd
from PIL import Image, ImageDraw

def create_pacman_frame(frame):
    img = Image.new('RGB', (16, 16), color='black')
    draw = ImageDraw.Draw(img)

    # Define the mouth angles for different frames
    mouth_angles = {
        1: (190, 170),  # Partially open
        2: (225, 135),  # More open
        3: (240, 120),  # Fully open
    }

    # Draw Pac-Man with varying mouth sizes
    draw.pieslice([(2, 2), (14, 14)], start=mouth_angles[frame][0], end=mouth_angles[frame][1], fill="yellow", outline="black")
    return img

def display_frame(image, offset_x=0):
    width, height = unicornhathd.get_shape()

    for x in range(width):
        for y in range(height):
            # Calculate the correct pixel position
            pixel_position = (width + image.width - x + offset_x) % (width + image.width)

            if pixel_position < width:
                pixel = image.getpixel((pixel_position, y))
                r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                unicornhathd.set_pixel(x, y, r, g, b)
            else:
                unicornhathd.set_pixel(x, y, 0, 0, 0)
    
    unicornhathd.show()

def animate_pacman():
    frames = [create_pacman_frame(i) for i in range(1, 4)]
    width, _ = unicornhathd.get_shape()

    try:
        while True:
            for offset in range(-16, width + 16):
                for frame in frames:
                    display_frame(frame, offset_x=offset)
                    time.sleep(0.1)
    except KeyboardInterrupt:
        unicornhathd.off()

unicornhathd.rotation(0)
unicornhathd.brightness(0.5)

animate_pacman()
