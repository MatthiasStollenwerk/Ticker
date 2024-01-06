#!/usr/bin/env python

import random
import time
import logging
try:
    import unicornhathd as unicornhathd
    logging.info('unicorn hat hd detected')
except ImportError:
    logging.info('unicorn hat hd not detected - using simulator')
    from unicorn_hat_sim import unicornhathd as unicornhathd
try:
    xrange
except NameError:
    xrange = range

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')        

unicornhathd.rotation(0)
unicornhathd.brightness(0.6)
width, height = unicornhathd.get_shape()
size = width * height
# Define color constants
COLOR_LIGHT_SLATE = [154, 154, 174]
COLOR_BLUE = [0, 0, 255]
COLOR_DARK_BLUE = [0, 0, 200]
COLOR_DARKER_BLUE = [0, 0, 160]
COLOR_VERY_DARK_BLUE = [0, 0, 140]
COLOR_ALMOST_BLACK = [0, 0, 90]
COLOR_EXTREMELY_DARK_BLUE = [0, 0, 60]
COLOR_BLACK = [0, 0, 0]

class GameOfLife:
    def __init__(self):
        self.board = [int(7 * random.getrandbits(1)) for _ in xrange(size)]
        # Use color constants in the list
        # self.color = [COLOR_LIGHT_SLATE, COLOR_BLUE, COLOR_DARK_BLUE, COLOR_DARKER_BLUE, COLOR_VERY_DARK_BLUE, COLOR_ALMOST_BLACK, COLOR_EXTREMELY_DARK_BLUE, COLOR_BLACK]

        # color palette with red tones
        self.red_color_palette = [(255, 255, 255), (255, 0, 0), (200, 0, 0), (160, 0, 0), (140, 0, 0), (90, 0, 0), (60, 0, 0), (0, 0, 0)]

        # color palette with green tones
        self.green_color_palette = [(255, 255, 255), (0, 255, 0), (0, 200, 0), (0, 160, 0), (0, 140, 0), (0, 90, 0), (0, 60, 0), (0, 0, 0)]

    def value(self, x, y):
        index = ((x % width) * height) + (y % height)
        return self.board[index]

    def neighbors(self, x, y):
        sum = 0
        for i in xrange(3):
            for j in xrange(3):
                if i == 1 and j == 1:
                    continue
                if self.value(x + i - 1, y + j - 1) == 0:
                    sum = sum + 1
        return sum

    def next_generation(self):
        new_board = [False] * size
        for i in xrange(width):
            for j in xrange(height):
                neigh = self.neighbors(i, j)
                lvl = self.value(i, j)
                if lvl == 0:
                    # 
                    if neigh < 2:
                        #  Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
                        new_board[i * height + j] = min(7, lvl + 1)
                    elif 2 <= neigh <= 3:
                        # Any live cell with two or three live neighbours lives on to the next generation.
                        new_board[i * height + j] = 0
                    else:
                        # Any live cell with more than three live neighbours dies, as if by overpopulation.
                        new_board[i * height + j] = min(7, lvl + 1)
                else:
                    if neigh == 3:
                        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                        new_board[i * height + j] = 0
                    else:
                        new_board[i * height + j] = min(7, lvl + 1)
        self.board = new_board

    # function to calculate the sum of all fields in the board
    def calculate_Board_Score(self):
        score = 0
        for i in xrange(size):
            score += self.board[i]
        return score

    def all_dead(self):
                # calulate sum of all fields in the board
        for i in xrange(size):
            if self.board[i] != 7:
                return False
        return True

    def show_board(self, isUp = True):
        # logging.info('show_board isup: ' + str(isUp))   
        if isUp:
            self.color = self.green_color_palette
        else:
            self.color = self.red_color_palette
        for i in xrange(width):
            for j in xrange(height):
                rgb = self.color[self.value(i, j)]
                unicornhathd.set_pixel(i, j, rgb[0], rgb[1], rgb[2])
        unicornhathd.show()

def animate_generations(generations = 10, time_between_generations = 0.5, duration = 60, animation_speed = 0.01, IsUp = True):
    logging.info('animate_generations')
    start_time = time.time()   
    time_up = False
    while True:
        life = GameOfLife()
        try:
            old_score = 0
            unchanged_score_count = 0
            while not life.all_dead():
                life.next_generation()
                new_score = life.calculate_Board_Score()
                if new_score == old_score:
                    unchanged_score_count += 1
                    if unchanged_score_count == 10:
                        break
                else:
                    unchanged_score_count = 0
                old_score = new_score
                life.show_board(isUp = IsUp)
                time.sleep(animation_speed)
                        
                logging.info('Time: ' + str(time.time() - start_time))
                if time.time() - start_time > duration:
                    logging.info('Time is up - exiting now ...')
                    time_up = True
                    break
        except KeyboardInterrupt:
            logging.info('KeyboardInterrupt - exiting now ...')
            unicornhathd.clear()
            unicornhathd.off()
        generations -= 1
        if generations == 0 or time_up:
            logging.info('Done with generations - exiting now ...')
            break
        time.sleep(time_between_generations)
        print("New Game of Life")
        
def main():
    animate_generations(  100, # number of generations, 0 for infinite
                                      3, # time between generations
                                      30,  # duration in seconds (0 for infinite
                                      0.1, # animation speed
                                      True) # True = up, False = down
if __name__ == "__main__":
    import os
    os.system('clear')
    main()