import pygame, sys
import screen_load
from pygame.locals import *

class Person:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move_y(self, ya):
        if screen_load.hitbox_detection(self.x, (self.y+ya)):  # is there a wall?
            self.y += ya  # moving on y

    def move_x(self, xa):
        if screen_load.hitbox_detection((self.x + xa), self.y):  # is there a wall?
            self.x += xa  # moving on x

    def end_of_word(self, max_x, max_y):  # border of window, can be done via constant
        if self.x == max_x:  # right conner
            return self.x, self.y
        if self.x == 0:  # left conner
            return self.x, self.y
        if self.y == max_y:  # down conner
            return self.x, self.y
        if self.y == 0:  # up conner
            return self.x, self.y


pygame.init()
DISPLAY_SURFACE = pygame.display.set_mode((1280, 960))  # need this numbers as variables or constants
pygame.display.set_caption('Hra') # 80 60 tiles na obrazovce
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        screen_load.load_level(1,DISPLAY_SURFACE)
        pygame.display.update()
