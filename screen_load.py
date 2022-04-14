# tato funkce zařizuje načtení textur na obrazovku, z obrázku levelu načte každý pixel který má přestavovat 1 "Tile" a podle barvy tohoto pixelu vytvoří na obrazovce obrázek textury 16x16
# tato funkce se zavolá kdykoli hráč přejde z 1 obrazovky na jinou

from re import X
import pygame, sys
from pygame.locals import *
import math
import os
from PIL import Image
import player


def load_level(level,gameDisplay): # rendruje level
    global im
    global image_level
    im = Image.open('levels\Static_Hitbox' + "\\" + level + ".png" )
    image_level = pygame.image.load(os.path.join('levels\Images' + "\\" + level + ".png"))
    gameDisplay.blit(image_level, (0,0))
    return image_level

def reload_level(gameDisplay):
    gameDisplay.blit(image_level, (0,0))

def hitbox_detection(x,y):
    x = x/16 # tahle funkce vrát true pokud se hráč může posunout na zadanou pozici a false pokud ne
    y = y/16
    rgb_im = im.convert('RGB')
    r, g, b = rgb_im.getpixel((x, y))
    if r == 255 and g == 255 and b == 255:
        return True
    elif r == 0 and g == 0 and b == 0:
        return False

def Render_Text(what, color, where, window):
    font = pygame.font.Font('Graphics/Fonts/Snes.ttf', 30)
    text = font.render(what, 1, pygame.Color(color))
    window.blit(text, where)

def clear_bit(surface,image,xa,ya,xb,yb):
    surface.blit(image, (xa,ya),(xa,ya,xb,yb))





