import pygame, sys
import screen_load
from pygame.locals import *
import os
from PIL import Image,ImageOps
import a_star_pathfinding
import random
import item


REACTION_SPACE = 24
CLEAN_OFFSET = 2
CLEAN_SIZE = 20



class Button:
    def __init__(self,type,x,y,level,connection):
        self.current_level = level
        self.type = type
        self.x = x
        self.y = y
        self.last_x = 0
        self.last_y = 0
        self.texture = pygame.image.load(os.path.join('Graphics\Item\\' + item.item_type(type).name + ".png"))
        self.pressed = False
        self.connection = connection
    
    def render(self,current_level,display):
        if current_level == self.current_level:
            display.blit(self.texture,(self.x,self.y))
    
    def clear(self,surface,image):
        surface.blit(image, (self.last_x-CLEAN_OFFSET,self.last_y-CLEAN_OFFSET),(self.last_x-CLEAN_OFFSET,self.last_y-CLEAN_OFFSET,CLEAN_SIZE,CLEAN_SIZE))
    
    def pressed(self,item_list):
        for i in item_list:
            if i.type == 2:
                if i.x+8 > self.x and i.x-8 < self.x:
                    if i.y+8 > self.y and i.y-8 < self.y:
                        self.pressed = True
                        self.texture = pygame.image.load(os.path.join('Graphics\Item\\' + item.item_type(self.type).name + "_DOWN.png"))
                        break
                    else:
                        self.pressed = False
                        self.texture = pygame.image.load(os.path.join('Graphics\Item\\' + item.item_type(self.type).name + ".png"))

                else:
                    self.pressed = False
                    self.texture = pygame.image.load(os.path.join('Graphics\Item\\' + item.item_type(self.type).name + ".png"))
