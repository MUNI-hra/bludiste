import pygame, sys
import screen_load
from pygame.locals import *
import os
from PIL import Image,ImageOps
import a_star_pathfinding
import random
import item


REACTION_SPACE = 24
CLEAN_OFFSET = 4
CLEAN_SIZE = 40



class Door:
    def __init__(self,type,x,y,level,connection):
        self.current_level = level
        self.type = type
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.texture = pygame.image.load(os.path.join('Graphics\Item\\' + item.item_type(type).name + ".png"))
        self.open = False
        self.connection = connection
    
    def render(self,current_level,display):
        if current_level == self.current_level:
            display.blit(self.texture,(self.x,self.y))
    
    def clear(self,surface,image):
        surface.blit(image, (self.last_x-CLEAN_OFFSET,self.last_y-CLEAN_OFFSET),(self.last_x-CLEAN_OFFSET,self.last_y-CLEAN_OFFSET,CLEAN_SIZE,CLEAN_SIZE))
    
    def open(self,button_list):
        for i in button_list:
            if i.connection == self.connection:
                if i.pressed == True:
                    self.open = True
                    self.texture = pygame.image.load(os.path.join('Graphics\Item\\' + item.item_type(self.type).name + "_OPEN.png"))
                else:
                    self.open = False
                    self.texture = pygame.image.load(os.path.join('Graphics\Item\\' + item.item_type(self.type).name + ".png"))
