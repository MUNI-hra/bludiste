from numpy import character
import pygame, sys
import screen_load
import player
import os
from pygame.locals import *
player_texture = pygame.image.load(os.path.join('Graphics\Player\player.png'))

clock = pygame.time.Clock()

pygame.init()
DISPLAY_SURFACE = pygame.display.set_mode((1280, 960))  # need this numbers as variables or constants
pygame.display.set_caption('Hra') # 80 60 tiles na obrazovce
character = player.Person()




while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        screen_load.load_level(1,DISPLAY_SURFACE)
        player.Person.render(character,player_texture,DISPLAY_SURFACE)
        pygame.display.update()
    clock.tick(60)
    
