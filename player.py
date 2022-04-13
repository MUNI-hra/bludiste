import pygame, sys
import screen_load
from pygame.locals import *
import os
from PIL import Image,ImageOps

SIZE_OF_SCREEN_BORDER = 16 # konstanta okraje obrazovky
MAX_ANIMATION_FRAME = 10 # kolik snímků má animace (1 snímek je 1/20 sekundy)
END_OF_FRAME = 5
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
SIZE_OF_CHARACTER = 32


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
        if self.x < SIZE_OF_SCREEN_BORDER:  # left conner
            return "Left"
        if self.y > max_y:  # down conner
            return "Down"
        if self.y < SIZE_OF_SCREEN_BORDER:  # up conner
            return "Up"

    def render(self,surface,direction,walking,animation_frame): # rendruje hráče 
        animation_frame +=1
        texture = pygame.image.load(os.path.join('Graphics\Player\Front.png')) #basic texture
        if animation_frame == MAX_ANIMATION_FRAME:
            animation_frame = 0



        if direction == RIGHT: # rendering player if he is facing right 
            if walking == True: # rendering animation of him walking
                if animation_frame <= END_OF_FRAME:
                    texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\side_walk.png')), True, False)
                if animation_frame > END_OF_FRAME:
                    texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\side.png')), True, False)
            if walking == False: #rendering player if he is not moving
                texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\side.png')), True, False)



        elif direction == UP: # rendering player if he is facing up
            if walking == True: # rendering animation of him walking
                if animation_frame <= END_OF_FRAME:
                    texture = pygame.image.load(os.path.join('Graphics\Player\Back_walk.png'))
                if animation_frame > END_OF_FRAME:
                    texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\Back_walk.png')), True, False)
            if walking == False:
                texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\Back.png')), True, False)



        elif direction == LEFT: # rendering player if he is facing left
            if walking == True: # rendering animation of him walking
                if animation_frame <= END_OF_FRAME:
                    texture = pygame.image.load(os.path.join('Graphics\Player\side_walk.png'))
                if animation_frame > END_OF_FRAME:
                    texture = pygame.image.load(os.path.join('Graphics\Player\side.png'))
            if walking == False: #rendering player if he is not moving
                texture = pygame.image.load(os.path.join('Graphics\Player\side.png'))



        elif direction == DOWN: # rendering player if he is facing down 
            if walking == True: # rendering animation of him walking
                if animation_frame <= END_OF_FRAME:
                    texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Player\Front_walk.png')), True, False)
                if animation_frame > END_OF_FRAME:
                    texture = pygame.image.load(os.path.join('Graphics\Player\Front_walk.png'))
            if walking == False: #rendering player if he is not moving
                texture = pygame.image.load(os.path.join('Graphics\Player\Front.png'))




        surface.blit(pygame.transform.scale(texture,(SIZE_OF_CHARACTER,SIZE_OF_CHARACTER)), (self.x,self.y))        
        return animation_frame