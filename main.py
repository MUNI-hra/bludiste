from numpy import character
import pygame, sys
import screen_load
import player
import os
from pygame.locals import *
import pygame_gui
import math
import json



Current_Screen = 0

screen_X = 1280
screen_Y = 960
move_speed = 3

Menu_Button_Size_X = 250
Menu_Button_Size_Y = 50
Menu_Button_Spacing = 100

player_texture = pygame.image.load(os.path.join('Graphics\Player\player.png'))
direction = True
clock = pygame.time.Clock()
game_started = False
current_level = "Level1"

pygame.init()
DISPLAY_SURFACE = pygame.display.set_mode((screen_X, screen_Y))  # need this numbers as variables or constants
manager = pygame_gui.UIManager((screen_X, screen_Y))
pygame.display.set_caption('Hra') # 80 60 tiles na obrazovce
character = player.Person()
player.Person.set_x(character,30)
player.Person.set_y(character,470)
pygame.key.set_repeat(1,100)

#Tady se definují všechny elementy starting menu:
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_X/2-Menu_Button_Size_X/2, screen_Y/2-Menu_Button_Size_Y/2), (Menu_Button_Size_X, Menu_Button_Size_Y)), text='Start', manager=manager)
#credits_button =pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_X/2-Menu_Button_Size_X/2, screen_Y/2-Menu_Button_Size_Y/2+Menu_Button_Spacing), (Menu_Button_Size_X, Menu_Button_Size_Y)), text='Credits', manager=manager)
#settings_button =pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_X/2-Menu_Button_Size_X/2, screen_Y/2-Menu_Button_Size_Y/2+Menu_Button_Spacing*2), (Menu_Button_Size_X, Menu_Button_Size_Y)), text='Settings', manager=manager)
quit_button =pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_X/2-Menu_Button_Size_X/2, screen_Y/2-Menu_Button_Size_Y/2+Menu_Button_Spacing), (Menu_Button_Size_X, Menu_Button_Size_Y)), text='Quit', manager=manager)





while True:
    time_delta = clock.tick(20)/1000.0
    for event in pygame.event.get():
        if game_started == True:    # tento kód se spustí jen když už hrajete hru (když v menu vyberete že chcete hrát)
            key_pressed_is = pygame.key.get_pressed() #kód na ovládání hráče
            if key_pressed_is[K_w] and key_pressed_is[K_d] and not key_pressed_is[K_a] and not key_pressed_is[K_s]:
                player.Person.move_y(character,-(math.sqrt(2)*move_speed))
                player.Person.move_x(character,(math.sqrt(2)*move_speed))
                break
            if not key_pressed_is[K_w] and key_pressed_is[K_d] and not key_pressed_is[K_a] and key_pressed_is[K_s]:
                player.Person.move_y(character,(math.sqrt(2)*move_speed))
                player.Person.move_x(character,(math.sqrt(2)*move_speed))
                break
            if not key_pressed_is[K_w] and not key_pressed_is[K_d] and key_pressed_is[K_a] and key_pressed_is[K_s]:
                player.Person.move_y(character,(math.sqrt(2)*move_speed))
                player.Person.move_x(character,-(math.sqrt(2)*move_speed))
                break
            if key_pressed_is[K_w] and not key_pressed_is[K_d] and key_pressed_is[K_a] and not key_pressed_is[K_s]:
                player.Person.move_y(character,-(math.sqrt(2)*move_speed))
                player.Person.move_x(character,-(math.sqrt(2)*move_speed))
                break
            if key_pressed_is[K_w]:
                player.Person.move_y(character,-move_speed)
            if key_pressed_is[K_a]:
                player.Person.move_x(character,-move_speed)
                direction = False
            if key_pressed_is[K_s]:
                player.Person.move_y(character,move_speed)
            if key_pressed_is[K_d]:
                player.Person.move_x(character,move_speed)
                direction = True

            if player.Person.end_of_word(character,screen_X-16,screen_Y-16) != None:
                js = open("levels\level_conection.json")
                data = json.load(js)
                next_level = data[current_level]
                if player.Person.end_of_word(character,screen_X-16,screen_Y-16) == "Left":
                    screen_load.load_level(next_level[0]["Left"],DISPLAY_SURFACE)
                    current_level = next_level[0]["Left"]
                elif player.Person.end_of_word(character,screen_X-16,screen_Y-16) == "Up":
                    screen_load.load_level(next_level[1]["Up"],DISPLAY_SURFACE)
                    current_level = next_level[1]["Up"]
                elif player.Person.end_of_word(character,screen_X-16,screen_Y-16) == "Down":
                    screen_load.load_level(next_level[2]["Down"],DISPLAY_SURFACE)
                    current_level = next_level[2]["Down"]
                elif player.Person.end_of_word(character,screen_X-16,screen_Y-16) == "Right":
                    screen_load.load_level(next_level[3]["Right"],DISPLAY_SURFACE)
                    current_level = next_level[3]["Right"]
                player.Person.set_x(character,int(data[current_level][4]["X"]))
                player.Person.set_y(character,int(data[current_level][5]["Y"]))
                    
#
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        

        if game_started == False: # ovládání tlačítek v menu
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    game_started = True
                elif event.ui_element == quit_button:
                    pygame.quit()
                    sys.exit()

    if game_started == True: # tento kód se spustí jen když už hrajete hru (když v menu vyberete že chcete hrát)
        screen_load.load_level(current_level,DISPLAY_SURFACE)
        player.Person.render(character,player_texture,DISPLAY_SURFACE,direction)


    if game_started == False: # tento kód ovládá menu
        image = pygame.image.load(os.path.join('Graphics\Menu\Background.jpg'))
        manager.process_events(event)
        manager.update(time_delta)
        DISPLAY_SURFACE.blit(image,(0,0))
        manager.draw_ui(DISPLAY_SURFACE)


    pygame.display.update()
    
