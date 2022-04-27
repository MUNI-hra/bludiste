from re import X
import pygame, sys
import math
import os
import player
import pygame, sys
import screen_load
from pygame.locals import *
import os
from PIL import Image,ImageOps
from enum import Enum
import enemy

REACTION_SPACE = 24
CLEAN_OFFSET = 2
CLEAN_SIZE = 20
all_items = []
all_enemies = []

class start_game(list):

    def start_game_definition():
        all_items = []
        return all_items

    def enemies_definition():
        all_enemies.append(enemy.Enemy("Level1",300,400))
        all_enemies.append(enemy.Enemy("Level1",400,400))
        all_enemies.append(enemy.Enemy("Level1",400,500))
        return all_enemies

    def item_definition():
        all_items.append(Item(2,300,400,"Level1")) #0 = textura, 0 = x, 0 = y, "level1" = v jakým levelu je
        all_items.append(Item(1,400,400,"Level1"))
        return all_items



class item_type(Enum):
    NONE = 0
    HEAL = 1
    BOX = 2


class Item:
    def __init__(self,type,x,y,level):
        self.x = x
        self.y = y
        self.last_x = 0
        self.last_y = 0
        self.current_level = level
        self.type = type
        self.lives = True
        self.texture = pygame.image.load(os.path.join('Graphics\Item\\' + item_type(type).name + ".png"))
    
    def player_interacted(self,x_player,y_player,player,level):
        if level == self.current_level:
            if self.type == 2:
                Item.set_x(self,x_player+8)
                Item.set_y(self,y_player-15)
            if self.type == 1:
                if player.health < 5:
                    player.health +=1
                    self.lives = False
                    self.x = -10
                    self.y = -10


    def is_touching_player(self,xplayer,yplayer,player,level):
        if xplayer > self.x-REACTION_SPACE and xplayer < self.x+REACTION_SPACE:
            if yplayer > self.y-REACTION_SPACE and yplayer < self.y+REACTION_SPACE:
                Item.player_interacted(self,xplayer,yplayer,player,level)
                return self


    def move_y(self, ya):
        if screen_load.hitbox_detection(self.x, (self.y+ya)):  # is there a wall?
            self.last_y = self.y
            self.y += ya  # moving on y

    def move_x(self, xa):
        if screen_load.hitbox_detection((self.x + xa), self.y):  # is there a wall?
            self.last_x = self.x
            self.x += xa  # moving on x
    
    def set_x(self, xpos): # nastaví x na pozici v absolutních souřadnicích
        self.x = xpos
        self.last_x = xpos
    
    def set_y(self, ypos): # nastaví y na pozici v absolutních souřadnicích
        self.y = ypos
        self.last_y = ypos
    
    def clear(self,surface,image):
        surface.blit(image, (self.last_x-CLEAN_OFFSET,self.last_y-CLEAN_OFFSET),(self.last_x-CLEAN_OFFSET,self.last_y-CLEAN_OFFSET,CLEAN_SIZE,CLEAN_SIZE))
    
    def render(self,current_level,display):
        if self.lives:
            if current_level == self.current_level:
                display.blit(self.texture,(self.x,self.y))
    
    
