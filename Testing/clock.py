import math
import time
import unicornhathd as uh

def draw_line(x0, y0, x1, y1, color):
    """Draws a line from (x0, y0) to (x1, y1) using Bresenham's Line Algorithm"""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            uh.set_pixel(x, y, *color)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            uh.set_pixel(x, y, *color)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    uh.set_pixel(x, y, *color)

def draw_hand(centerX, centerY, length, angle, color):
    endX = int(centerX + length * math.sin(math.radians(angle)))
    endY = int(centerY - length * math.cos(math.radians(angle)))
    draw_line(centerX, centerY, endX, endY, color)

def update_clock():
    uh.clear()
    centerX, centerY = 7, 7
    now = time.localtime()
    hours, minutes, seconds = now.tm_hour, now.tm_min, now.tm_sec

    # Calculate angles for each hand
    hour_angle = ((hours % 12) / 12) * 360 + (minutes / 60) * 30
    minute_angle = (minutes / 60) * 360
    second_angle = (seconds / 60) * 360

    # Draw each hand
    draw_hand(centerX, centerY, 3, hour_angle, [255, 0, 0])  # Red for hour hand
    draw_hand(centerX, centerY, 5, minute_angle, [0, 255, 0])  # Green for minute hand
    draw_hand(centerX, centerY, 6, second_angle, [0, 0, 255])  # Blue for second hand

    uh.show()

uh.set_layout(uh.HAT)
uh.brightness(0.5)
uh.rotation(270)

while True:
    update_clock()
    time.sleep(1)
