import pygame, sys
import screen_load
from pygame.locals import *
import os
from PIL import Image,ImageOps


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
    
    def set_x(self, xpos): # nastaví x na pozici v absolutních souřadnicích
        self.x = xpos
    
    def set_y(self, ypos): # nastaví y na pozici v absolutních souřadnicích
        self.y = ypos


    def end_of_word(self, max_x, max_y):  # border of window, can be done via constant
        if self.x > max_x:  # right conner
            return "Right"
        if self.x < 16:  # left conner
            return "Left"
        if self.y > max_y:  # down conner
            return "Down"
        if self.y < 16:  # up conner
            return "Up"

    def render(self,surface,direction,walking,animation_frame): # rendruje hráče 
        animation_frame +=2
        texture = pygame.image.load(os.path.join('Graphics\Player\Front.png'))
        if animation_frame == 20:
            animation_frame = 0
        if direction == 0:
            if walking == True:
                if animation_frame <= 10:
                    texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\side_walk.png')), True, False)
                if animation_frame > 10:
                    texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\side.png')), True, False)
            if walking == False:
                texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\side.png')), True, False)

        elif direction == 1:
            if walking == True:
                if animation_frame <= 10:
                    texture = pygame.image.load(os.path.join('Graphics\Player\Back_walk.png'))
                if animation_frame > 10:
                    texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\Back_walk.png')), True, False)
            if walking == False:
                texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\Back.png')), True, False)

        elif direction == 2:
            if walking == True:
                if animation_frame <= 10:
                    texture = pygame.image.load(os.path.join('Graphics\Player\side_walk.png'))
                if animation_frame > 10:
                    texture = pygame.image.load(os.path.join('Graphics\Player\side.png'))
            if walking == False:
                texture = pygame.image.load(os.path.join('Graphics\Player\side.png'))

        elif direction == 3:
            if walking == True:
                if animation_frame <= 10:
                    texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\Front_walk.png')), True, False)
                if animation_frame > 10:
                    texture = pygame.image.load(os.path.join('Graphics\Player\Front_walk.png'))
            if walking == False:
                texture = pygame.image.load(os.path.join('Graphics\Player\Front.png'))

        surface.blit(pygame.transform.scale(texture,(32,32)), (self.x,self.y))        
        return animation_frame