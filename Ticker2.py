#!/usr/bin/env python
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s  :  %(message)s')

import colorsys
import time
from sys import exit
import yfinance as yf
from colorama import Fore, Style
from datetime import datetime
import pytz
import holidays
from PIL import Image, ImageDraw
import os
import gameOfLife
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')
try:
    import unicornhathd as unicornhathd
    logging.info('unicorn hat hd detected')
    logging.debug('Setting unicorn hat rotation and brightness to 90 and 0.6')
    unicornhathd.rotation(90)
except ImportError:
    logging.info('unicorn hat hd not detected - using simulator')
    # import unicorn_hat_sim-xxx as unicornhathd
    from unicorn_hat_sim import unicornhathd as unicornhathd
    logging.debug('Setting unicorn hat rotation and brightness to 90 and 0.6')
    
    unicornhathd.rotation(0)

## 
#    PacMan Stuff
##
# Define the mouth angles for different frames
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
    # If the stock is up, create a series of yellow Pacman frames
    if IsStockUp:
        frames = [create_pacman_frame(i, "yellow") for i in range(1, 4)]
    else:
        # If the stock is down, create a series of blue Pacman frames
        frames = [create_pacman_frame(i, "blue") for i in range(1, 4)]

    # Get the width of the unicorn hat
    width, _ = unicornhathd.get_shape()

    # Loop over the range from negative width to width
    for offset in range(-width, width):
        # For each frame in the frames list
        for frame in frames:
            # Display the frame with the current offset
            display_pacman_frame(frame, offset_x=offset)
            # Sleep for 0.05 seconds to create the animation effect
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

# Get the stock information for a given ticker symbol
def get_stock_info(ticker_symbol):
    message = ""
    color = (255,255,255)

    try:
        exchangeOpen = is_nyse_open()
        logging.debug(f"NYSE is open: {exchangeOpen}")

        IsStockUp = True

        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.info
        if 'currentPrice' in stock_info and 'currency' in stock_info:
            current = stock_info['currentPrice']
            open = stock_info['open']
            delta = round(current - open,2)
            message = f"+++ {ticker_symbol} : {stock_info['currentPrice']} {stock_info['currency']} +++ Open : {stock_info['open']} +++ Delta : {delta} {stock_info['currency']} +++"

            logging.debug(f"message: {message}")

            if current >= open:
                IsStockUp = True
                color = (0,255,0) if exchangeOpen else (64, 224, 208)
                print(f"{Fore.GREEN}{message} {Fore.RESET}")
            elif current < open:
                IsStockUp = False
                print(f"{Fore.RED}{message} {Fore.RESET}")
                color = (255,0,0) if exchangeOpen else (255, 192, 203)
            logging.debug(f"IsStockUp: {IsStockUp}")
        else:
            message = f"+++ {ticker_symbol} : Price information not available. +++"
            logging.error(message)
        return message, color, IsStockUp
    except Exception as e:
        logging.error(f"Error getting stock info: {e}")
        return f"An error occurred: {e}", (255,255,255), True

def animate_image(image, delay=0.03):
    logging.debug('Starting animate_image function')
    # Get the width of the image
    imageWidth = image.width

    # Set the width and height of the unicorn hat
    width = height = 16

    # Loop over the width of the image
    for scroll in range(imageWidth - width):
        # Loop over the width of the unicorn hat
        for x in range(width):
            # Loop over the height of the unicorn hat
            for y in range(height):
                # Get the pixel at the current x and y position
                pixel = image.getpixel((x + scroll, y))

                # Check if the pixel has three values (RGB)
                if len(pixel) == 3: 
                    # If it does, unpack the values into r, g, and b
                    r, g, b = [int(n) for n in pixel]
                else:
                    # If it has four values (RGBA), unpack the values into r, g, b, and bg
                    r, g, b, bg = [int(n) for n in pixel]

                # Set the pixel at the current x and y position on the unicorn hat to the r, g, and b values
                unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

        # Show the updated pixels on the unicorn hat
        unicornhathd.show()

        # Sleep for the specified delay
        time.sleep(delay)
    # unicornhathd.clear()
    # unicornhathd.off()
    logging.debug('Animate image function finished. Turning off unicorn hat')

def animate_message (message, color, delay=0.03):
    logging.debug('Starting animate_message function')
    # Get the width and height of the unicorn hat
    width, height = unicornhathd.get_shape()
    # Initialize the x position of the text
    text_x = width
    # Initialize the y position of the text
    text_y = 2

    # Initialize an empty list for lines of text
    lines = [""]
    # Set the font for the text
    try:
        current_dir = os.getcwd()
        # Try to use the Roboto font
        FONT = (f'{current_dir}/Roboto-Bold.ttf', 16) 
        font_file, font_size = FONT
        font = ImageFont.truetype(font_file, font_size)
    except Exception as e:
        logging.error(f"Error loading font: {e}")
        return

    # Initialize the width and height of the text
    text_width, text_height = width, 0
    try:
        # Set the first line of the text
        lines[0]= message
        text_width =0

        # Calculate the width and height of the text
        for line in lines:
            #w, h = font.getsize(line)
            #text_width += w + width
            #text_height = max(text_height, h)
            bbox = font.getbbox(line)
            text_width += bbox[2] + width
            text_height = max(text_height, bbox[3])

        # Add the width of the text and the x position of the text
        text_width += width + text_x + 1
        # Create a new image with the calculated width and height
        image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Initialize the left offset
        offset_left = 0
        # Draw each line of the text on the image
        for index, line in enumerate(lines):
            draw.text((text_x + offset_left, text_y-3), line, color, font=font)
            # offset_left += font.getsize(line)[0] + width
            offset_left += font.getbbox(line)[2] + width

        # Animate the image
        animate_image(image, delay)

    except KeyboardInterrupt:
        # If the script is interrupted, turn off the unicorn hat
        unicornhathd.off()
        logging.debug('Keyboard interrupt, turning off unicorn hat')
    finally:
        # Ensure the unicorn hat is turned off
        # unicornhathd.off()
        logging.debug('Animate message function finished. Turning off unicorn hat')

# Load an image from a file
def load_image(filename):
    return Image.open(filename)

def load_images():
    try:
        logging.debug('Loading mushroom and shell images')  
        current_dir = os.getcwd()
        logging.debug(f"Current directory: {current_dir}")
        mushroom = load_image(f"{current_dir}/mushroom.png")
        shell = load_image(f"{current_dir}/shell.png")  
        return mushroom, shell
    except Exception as e:
        logging.error(f"Error getting current directory: {e}")
        return None, None

# Main function
def main():

    try:
        logging.debug('Starting main function')
        unicornhathd.brightness(0.6)
        mushroom = shell = None

       # Load the images for the mushroom and shell
        try:
            logging.debug('Loading mushroom and shell images')  
            current_dir = os.getcwd()
            logging.debug(f"Current directory: {current_dir}")  
            mushroom, shell = load_images()
        except FileNotFoundError as e:
            logging.error(f"Error loading images: {e}")
            return
        
        # Main loop
        logging.debug('Entering main loop')
        while True:
            try:
                # Set the default background color
                backgroundColor = (0, 0, 0)
                
                # Check if the NYSE is open
                logging.debug('Checking if NYSE is open')
                exchangeIsOpen = is_nyse_open()

                if exchangeIsOpen:
                    logging.debug('NYSE is open')
                    textColor = (0, 255, 0)
                    animate_message("+++ NYSE is OPEN +++", textColor)
                    logging.debug("showtime=1")
                    showTime=1
                else:
                    logging.debug('NYSE is closed')
                    textColor = (255, 0 , 0)
                    animate_message("+++ NYSE is CLOSED +++", textColor)
                    showTime=2
                    logging.debug("showtime=2")
                IsUp = True
                try:
                    logging.debug('Getting stock info for MSFT')
                    message, textColor, IsUp = get_stock_info("MSFT")
                except Exception as e:
                    message = f"Unexpected error from get_stock_info : {e}"
                    textColor = (255, 0, 0)
                    logging.error(f"Error getting stock info: {e}")
            
                logging.debug('Animating mushroom') if IsUp else logging.debug('Animating shell')  
                animate_image(mushroom) if IsUp else animate_image(shell)   

                logging.debug(f'Animating Stock message {message}')    
                animate_message(message, textColor)

                logging.debug(f'Animating time {showTime} times')       
                for i in range (showTime):
                    now = datetime.now()
                    current_time = now.strftime("%H:%M")
                    logging.debug(f"Animating time: {current_time}")
                    animate_message(f"{current_time}", (255,255,255),0.1)
                    logging.debug('Animating pacman')
                    animate_pacman(IsUp)
                    if exchangeIsOpen:
                        gameOfLife.animate_generations( 10, 3, 30, 0.1)
                    else:
                        gameOfLife.animate_generations( 10, 3, 120, 0.1)
                
            except KeyboardInterrupt:
                logging.debug('Keyboard interrupt, turning off unicorn hat')
                return
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                return  
    except KeyboardInterrupt:
        # If the script is interrupted, turn off the unicorn hat
        unicornhathd.off()
    except Exception as e:
        print(f"Unexpected error: {e}")
        unicornhathd.off()

if __name__ == "__main__":
    # Clear the terminal
    os.system('clear')

    logging.debug('Calling main function')
    main()
    logging.debug('Stopped main function')  
