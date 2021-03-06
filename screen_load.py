# tato funkce zařizuje načtení textur na obrazovku, z obrázku levelu načte každý pixel který má přestavovat 1 "Tile" a podle barvy tohoto pixelu vytvoří na obrazovce obrázek textury 16x16
# tato funkce se zavolá kdykoli hráč přejde z 1 obrazovky na jinou

from re import X
import pygame, sys
from pygame.locals import *
import math
import os
from PIL import Image
import player

RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3


def load_level(level,gameDisplay): # rendruje level
    global im
    global image_level
    im = Image.open('levels\Static_Hitbox' + "\\" + level + ".png" )
    image_level = pygame.image.load(os.path.join('levels\Images' + "\\" + level + ".png"))
    gameDisplay.blit(image_level, (0,0))
    return im, image_level

def load_level_array(im):
    level_array = []
    rgb_im = im.convert('RGB')
    for i in range(80):
        level_array.append([])
        for j in range(60):
            r, g, b = rgb_im.getpixel((i, j))
            if r == 0 and g == 0 and b == 0:
                level_array[i].append(1)
            else:
                level_array[i].append(0)

    return level_array

def reload_level(gameDisplay):
    gameDisplay.blit(image_level, (0,0))

def hitbox_detection(x,y,facing,door_list):
    x = x/16 # tahle funkce vrát true pokud se hráč může posunout na zadanou pozici a false pokud ne
    y = y/16
    rgb_im = im.convert('RGB')
    r, g, b = rgb_im.getpixel((x, y))
    for i in door_list:
        if i.open == False:
            if i.x+16 > x*16 and i.x < x*16:
                if i.y+16 > y*16 and i.y < y*16:
                    return False
    if r == 255 and g == 255 and b == 255:
        return True
    elif r == 0 and g == 0 and b == 0:
        return False
    elif r == 0 and g == 8 and b == 255 and facing == RIGHT:
        return "Jump Right"
    elif r == 0 and g == 255 and b == 244 and facing == DOWN:
        return "Jump Down"
    elif r == 53 and g == 255 and b == 0 and facing == UP:
        return "Jump Up"
    elif r == 255 and g == 145 and b == 0 and facing == LEFT:
        return "Jump Left"

def Render_Text(what, color, where, window):
    font = pygame.font.Font('Graphics/Fonts/Snes.ttf', 30)
    text = font.render(what, 1, pygame.Color(color))
    window.blit(text, where)

def clear_bit(surface,image,xa,ya,xb,yb):
    surface.blit(image, (xa,ya),(xa,ya,xb,yb))

def Render_Health(self,surface,bar,pointer):
    surface.blit(pygame.transform.scale(bar,(200,60)), (0,30))
    surface.blit(pygame.transform.scale(pointer,(16,16)), (self.health*22+48,70))



