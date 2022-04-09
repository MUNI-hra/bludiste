from numpy import character
import pygame, sys
import screen_load
import player
import os
from pygame.locals import *
import pygame_gui

screen_X = 1280
screen_Y = 960

move_speed = 4

Menu_Button_Size_X = 250
Menu_Button_Size_Y = 50

player_texture = pygame.image.load(os.path.join('Graphics\Player\player.png'))
direction = True
clock = pygame.time.Clock()
game_started = False

pygame.init()
DISPLAY_SURFACE = pygame.display.set_mode((screen_X, screen_Y))  # need this numbers as variables or constants
manager = pygame_gui.UIManager((screen_X, screen_Y))
pygame.display.set_caption('Hra') # 80 60 tiles na obrazovce
character = player.Person()
player.Person.set_x(character,30)
player.Person.set_y(character,470)

#Tady se definují všechny elementy starting menu:
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_X/2-Menu_Button_Size_X/2, screen_Y/2-Menu_Button_Size_Y/2), (Menu_Button_Size_X, Menu_Button_Size_Y)), text='Start', manager=manager)







while True:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if game_started == True:    # tento kód se spustí jen když už hrajete hru (když v menu vyberete že chcete hrát)
            key_pressed_is = pygame.key.get_pressed() #kód na ovládání hráče
            if key_pressed_is[K_w]:
                player.Person.move_y(character,-move_speed)
            if key_pressed_is[K_a]:
                player.Person.move_x(character,-move_speed)
            if key_pressed_is[K_s]:
                player.Person.move_y(character,move_speed)
            if key_pressed_is[K_d]:
                player.Person.move_x(character,move_speed)
            
            if event.type == pygame.KEYDOWN: #kód na otáčení hráče podle směru chůze
                if event.key == pygame.K_d:
                    direction = True
                elif event.key == pygame.K_a:
                    direction = False
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if game_started == False: # ovládání tlačítek v menu
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == start_button:
                  game_started = True




    if game_started == True: # tento kód se spustí jen když už hrajete hru (když v menu vyberete že chcete hrát)
        screen_load.load_level(1,DISPLAY_SURFACE)
        player.Person.render(character,player_texture,DISPLAY_SURFACE,direction)


    if game_started == False: # tento kód ovládá menu
        image = pygame.image.load(os.path.join('Graphics\Menu\Background.jpg'))
        manager.process_events(event)
        manager.update(time_delta)
        DISPLAY_SURFACE.blit(image,(0,0))
        manager.draw_ui(DISPLAY_SURFACE)


    pygame.display.update()
    
