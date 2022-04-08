# tato funkce zařizuje načtení textur na obrazovku, z obrázku levelu načte každý pixel který má přestavovat 1 "Tile" a podle barvy tohoto pixelu vytvoří na obrazovce obrázek textury 16x16
# tato funkce se zavolá kdykoli hráč přejde z 1 obrazovky na jinou

from re import X
import pygame, sys
from pygame.locals import *
import math
import PIL
import os
from PIL import Image


def load_level(level,gameDisplay):
    if level == 1:
        image_level = pygame.image.load(os.path.join('levels\Images\level1.png'))
        gameDisplay.blit(image_level, (0,0))
    if level == 2:
        image_level = pygame.image.load(os.path.join('levels\Images\level1.png'))
        gameDisplay.blit(image_level, (0,0))

def hitbox_detection(x,y):
    x = x/16 # tahle funkce vrát true pokud se hráč může posunout na zadanou pozici a false pokud ne
    y = y/16
    im = Image.open('levels\Static_Hitbox\level1.png')
    rgb_im = im.convert('RGB')
    r, g, b = rgb_im.getpixel((x, y))
    print(r,g,b)
    if r == 255 and g == 253 and b == 253:
        return True
    elif r == 0 and g == 0 and b == 0:
        return False



print(hitbox_detection(640,640))



