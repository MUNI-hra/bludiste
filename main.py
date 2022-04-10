from numpy import character
import pygame, sys
import screen_load
import player
import os
from pygame.locals import *
import pygame_gui
import math
import json


animation_frame = 0

screen_X = 1280 #velikosti obrazovky
screen_Y = 960

move_speed = 3 #rychlost chůze hráče v pixelech za krok (default je 3)

Menu_Button_Size_X = 250 #rozměry a rozložení tlačítek v menu
Menu_Button_Size_Y = 50
Menu_Button_Spacing = 100

direction = 0 #směr hráče 0 = doprava, 1 = nahorů, 2 = doleva, 3 = dolů
walking = False # je true pokud se hráč pohybuje
clock = pygame.time.Clock() # časovač na ovládání fps
game_started = False # nastaví se na true pokud nejsem v menu
current_level = "Level1" # level na kterým se začíná

pygame.init() #init hry
DISPLAY_SURFACE = pygame.display.set_mode((screen_X, screen_Y))  # need this numbers as variables or constants
manager = pygame_gui.UIManager((screen_X, screen_Y)) #manager na ovládání menu
pygame.display.set_caption('Hra') # 80 60 tiles na obrazovce
character = player.Person() # objekt ve třídě hráče
player.Person.set_x(character,30) #starting pozice hráče
player.Person.set_y(character,470)
pygame.key.set_repeat(1,100) # vypne auto repeat na klavesnici

#Tady se definují všechny elementy starting menu:
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_X/2-Menu_Button_Size_X/2, screen_Y/2-Menu_Button_Size_Y/2), (Menu_Button_Size_X, Menu_Button_Size_Y)), text='Start', manager=manager)
quit_button =pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_X/2-Menu_Button_Size_X/2, screen_Y/2-Menu_Button_Size_Y/2+Menu_Button_Spacing), (Menu_Button_Size_X, Menu_Button_Size_Y)), text='Quit', manager=manager)



while True: # tady začíná hlavní herní loop
    time_delta = clock.tick(20)/1000.0 # časovač pro menu elementy
    for event in pygame.event.get(): #ovládání eventů
        if game_started == True:    # tento kód se spustí jen když už hrajete hru (když v menu vyberete že chcete hrát)
            key_pressed_is = pygame.key.get_pressed() #kód na ovládání hráče
                # první 4 if jsou na úhlopříčky a ty další 4 na rovný směry

            if key_pressed_is[K_w] and key_pressed_is[K_d] and not key_pressed_is[K_a] and not key_pressed_is[K_s]:
                player.Person.move_y(character,-(math.sqrt(2)*move_speed))
                player.Person.move_x(character,(math.sqrt(2)*move_speed))
                direction = 0
                walking = True
                break
            if not key_pressed_is[K_w] and key_pressed_is[K_d] and not key_pressed_is[K_a] and key_pressed_is[K_s]:
                player.Person.move_y(character,(math.sqrt(2)*move_speed))
                player.Person.move_x(character,(math.sqrt(2)*move_speed))
                direction = 0
                walking = True
                break
            if not key_pressed_is[K_w] and not key_pressed_is[K_d] and key_pressed_is[K_a] and key_pressed_is[K_s]:
                player.Person.move_y(character,(math.sqrt(2)*move_speed))
                player.Person.move_x(character,-(math.sqrt(2)*move_speed))
                direction = 2
                walking = True
                break
            if key_pressed_is[K_w] and not key_pressed_is[K_d] and key_pressed_is[K_a] and not key_pressed_is[K_s]:
                player.Person.move_y(character,-(math.sqrt(2)*move_speed))
                player.Person.move_x(character,-(math.sqrt(2)*move_speed))
                direction = 2
                walking = True
                break
            if key_pressed_is[K_w]:
                player.Person.move_y(character,-move_speed)
                walking = True
                direction = 1
            if key_pressed_is[K_a]:
                player.Person.move_x(character,-move_speed)
                walking = True
                direction = 2
            if key_pressed_is[K_s]:
                player.Person.move_y(character,move_speed)
                walking = True
                direction = 3
            if key_pressed_is[K_d]:
                player.Person.move_x(character,move_speed)
                walking = True
                direction = 0
            if not key_pressed_is[K_d] and not key_pressed_is[K_a] and not key_pressed_is[K_s] and not key_pressed_is[K_w]:
                walking = False

            if player.Person.end_of_word(character,screen_X-16,screen_Y-16) != None: # ovládání screen wrappingu
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
                    

        if event.type == QUIT: # vypínání hry
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
        screen_load.load_level(current_level,DISPLAY_SURFACE) # načte texturu levelu
        animation_frame = player.Person.render(character,DISPLAY_SURFACE,direction,walking,animation_frame) # načte texturu hráče


    if game_started == False: # tento kód ovládá menu
        image = pygame.image.load(os.path.join('Graphics\Menu\Background.jpg'))
        manager.process_events(event)
        manager.update(time_delta)
        DISPLAY_SURFACE.blit(image,(0,0))
        manager.draw_ui(DISPLAY_SURFACE)


    pygame.display.update() # update obrazovky
    
