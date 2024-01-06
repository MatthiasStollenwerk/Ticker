#!/usr/bin/env python

import colorsys
import logging
import time
from sys import exit
import yfinance as yf
from colorama import Fore, Style
from datetime import datetime
import pytz
import holidays
from PIL import Image, ImageDraw

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

try:
    import unicornhathd as unicornhathd
    print("unicorn hat hd detected")
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicornhathd

logging.basicConfig(filename='program.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

## 
#    PacMan Stuff
##
def create_pacman_frame(frame, color):
    img = Image.new('RGB', (16, 16), color='black')
    draw = ImageDraw.Draw(img)

    # Define the mouth angles for different frames
    mouth_angles = {
        1: (190, 170),  # Partially open
        2: (225, 135),  # More open
        3: (240, 120),  # Fully open
    }

    # Draw Pac-Man with varying mouth sizes
    draw.pieslice([(2, 2), (14, 14)], start=mouth_angles[frame][0], end=mouth_angles[frame][1], fill=color, outline="black")
    return img

def display_pacman_frame(image, offset_x=0):
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
                unicornhathd.set_pixel(x, y, 0, 0, 0)
    
    unicornhathd.show()

def animate_pacman(IsStockUp):
    if IsStockUp:
        frames = [create_pacman_frame(i, "yellow") for i in range(1, 4)]
    else:
        frames = [create_pacman_frame(i, "blue") for i in range(1, 4)]

    width, _ = unicornhathd.get_shape()

    for offset in range(-width, width):
        for frame in frames:
            display_pacman_frame(frame, offset_x=offset)
            time.sleep(0.05)

## 
#    Stock Stuff
##

def is_nyse_open():
    # NYSE timezone
    nyse_tz = pytz.timezone('America/New_York')

    # Current time in NYSE timezone
    current_time_ny = datetime.now(nyse_tz)

    # Check if today is a weekend
    if current_time_ny.weekday() > 4:  # 0 is Monday, 6 is Sunday
        return False

    # Check for public holidays
    us_holidays = holidays.US()
    if current_time_ny.strftime('%Y-%m-%d') in us_holidays:
        return False

    # NYSE opening and closing times
    opening_time = nyse_tz.localize(datetime(current_time_ny.year, current_time_ny.month, current_time_ny.day, 9, 30))
    closing_time = nyse_tz.localize(datetime(current_time_ny.year, current_time_ny.month, current_time_ny.day, 16, 0))

    # Check if current time is within trading hours
    return opening_time <= current_time_ny <= closing_time

def get_stock_info(ticker_symbol):
    message = ""
    color = (255,255,255)

    try:
        exchangeOpen = is_nyse_open()
        print("NYSE is open" if exchangeOpen else "NYSE is closed.")

        IsStockUp = True

        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.info
        if 'currentPrice' in stock_info and 'currency' in stock_info:
            current = stock_info['currentPrice']
            open = stock_info['open']
            delta = round(current - open,2)
            message = f"+++ {ticker_symbol} : {stock_info['currentPrice']} {stock_info['currency']} +++ Open : {stock_info['open']} +++ Delta : {delta} {stock_info['currency']} +++"

            if current >= open:
                IsStockUp = True
                if exchangeOpen:
                    # Green
                    color = (0,255,0)
                else: 
                    #Pink
                    color = (64, 224, 208)
                print(f"{Fore.GREEN}{message} {Fore.RESET}")
            elif current < open:
                IsStockUp = False
                print(f"{Fore.RED}{message} {Fore.RESET}")
                if exchangeOpen:
                    # Red
                    color = (255,0,0)
                else:
                    #Pink
                    color = (255, 192, 203)
                    
            #print(f"{Fore.BLUE}Price: {stock_info['currentPrice']} {stock_info['currency']}{Style.RESET_ALL}")
            #print(f"Change: {stock_info['regularMarketChange']} {stock_info['currency']} ({stock_info['regularMarketChangePercent']:.2f}%)")
        else:
            print("Price information not available.")
        
        return message, color, IsStockUp
    except Exception as e:
        print("An error occurred:", e)
        print("Could not fetch stock information.")

def animate_image(image, delay=0.03):
        imageWidth = image.width
        width = height = 16
        for scroll in range(imageWidth - width):
            for x in range(width):
                for y in range(height):
                    pixel = image.getpixel((x + scroll, y))
                    if len(pixel) == 3: 
                        r, g, b = [int(n) for n in pixel]
                    else:
                        r, g, b,bg = [int(n) for n in pixel]
                    unicornhathd.set_pixel(width - 1 - x, y, r, g, b)
            unicornhathd.show()
            time.sleep(delay)

def animate_message (message, color, delay=0.03):
    width, height = unicornhathd.get_shape()
    text_x = width
    text_y = 2
    font_file, font_size = FONT
    font = ImageFont.truetype(font_file, font_size)
    text_width, text_height = width, 0
    try:
        lines[0]= message
        text_width =0

        for line in lines:
            w, h = font.getsize(line)
            text_width += w + width
            text_height = max(text_height, h)

        text_width += width + text_x + 1
        image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        offset_left = 0
        for index, line in enumerate(lines):
            draw.text((text_x + offset_left, text_y), line, color, font=font)
            offset_left += font.getsize(line)[0] + width

        animate_image(image, delay)

    except KeyboardInterrupt:
        unicornhathd.off()
    finally:
        unicornhathd.off()

def load_image(filename):
    return Image.open(filename)

## 
##      Main
##

lines = [""]
# FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 12)
FONT = ('/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf', 14)

unicornhathd.rotation(90)
unicornhathd.brightness(0.6)

try:
    mushroom = load_image("/home/mstoll/Learning/unicorn-hat-hd/mstoll/mushroom.png")
    shell = load_image("/home/mstoll/Learning/unicorn-hat-hd/mstoll/shell.png")

    while True:
        backgroundColor = (0, 0, 0)
        
        if is_nyse_open():
            textColor = (0, 255, 0)
            animate_message("+++ NYSE is OPEN +++", textColor)
            showTime=1
        else:
            textColor = (255, 0 , 0)
            animate_message("+++ NYSE is CLOSED +++", textColor)
            showTime=2
        IsUp = True
        # Get Stock information
        message, textColor, IsUp = get_stock_info("MSFT")
        if IsUp:
            animate_image(mushroom)
        else:
            animate_image(shell)

        animate_message(message, textColor)

        for i in range (showTime):
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            animate_message(f"{current_time}", (255,255,255),0.1)
            animate_pacman(IsUp)
      
except KeyboardInterrupt:
    unicorn.off()



