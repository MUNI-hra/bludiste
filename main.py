from numpy import character
import pygame, sys
import screen_load
import player
import os
from pygame.locals import *
import pygame_gui
import math
import json
import item
import enemy
import a_star_pathfinding
import button
import door
import goon


UP = 1
RIGHT = 0
LEFT = 2
DOWN = 3

SWORD_ANIMATION_LENGHT = 30

MAX_TIME_TO_NEXT_ATTACK = 200

second_clock = 0

render_list = []
enemie_list = []
item_list = []
button_list = []
door_list = []

item_list = item_list + item.start_game.item_definition()
enemie_list =enemie_list + item.start_game.enemies_definition()
button_list =button_list + item.start_game.button_definition()
door_list = door_list + item.start_game.door_definition()
boss = item.start_game.boss_definition()
render_list =render_list + button_list + item.start_game.start_game_definition() + item_list + door_list + enemie_list
render_list.append(boss)
holding = None

animation_frame = 0

sword_animation_frame = 0
sword_used = False
sword_angle = 0

screen_X = 1280 #velikosti obrazovky
screen_Y = 960

move_speed = 1 #rychlost chůze hráče v pixelech za krok (default je 3)
two_sqrt = math.sqrt(2)

Menu_Button_Size_X = 250 #rozměry a rozložení tlačítek v menu
Menu_Button_Size_Y = 50
Menu_Button_Spacing = 100

direction = 0 #směr hráče 0 = doprava, 1 = nahorů, 2 = doleva, 3 = dolů
walking = False # je true pokud se hráč pohybuje
clock = pygame.time.Clock() # časovač na ovládání fps
game_started = False # nastaví se na true pokud nejsem v menu
current_level = "Level1" # level na kterým se začíná
loaded_level =None

pygame.init() #init hry
DISPLAY_SURFACE = pygame.display.set_mode((screen_X, screen_Y),0,32)  # need this numbers as variables or constants
manager = pygame_gui.UIManager((screen_X, screen_Y)) #manager na ovládání menu
pygame.display.set_caption('Hra') # 80 60 tiles na obrazovce
character = player.Person() # objekt ve třídě hráče
player.Person.set_x(character,30) #starting pozice hráče 30
player.Person.set_y(character,470) # 470
pygame.key.set_repeat(1,100) # vypne auto repeat na klavesnici

#Tady se definují všechny elementy starting menu:
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_X/2-Menu_Button_Size_X/2, screen_Y/2-Menu_Button_Size_Y/2), (Menu_Button_Size_X, Menu_Button_Size_Y)), text='Start', manager=manager)
quit_button =pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_X/2-Menu_Button_Size_X/2, screen_Y/2-Menu_Button_Size_Y/2+Menu_Button_Spacing), (Menu_Button_Size_X, Menu_Button_Size_Y)), text='Quit', manager=manager)

level_hitbox, level_image = screen_load.load_level(current_level,DISPLAY_SURFACE)

level_array = screen_load.load_level_array(level_hitbox)
sword_texture = pygame.image.load(os.path.join("Graphics\Sword\Sword.png"))

healthbar_texture = pygame.image.load(os.path.join("Graphics\Health\Bar.png"))
healthbar_pointer_texture = pygame.image.load(os.path.join("Graphics\Health\Pointer.png"))


def render_everything():
    if game_started == True:
        boss.pathfind(character.x,character.y,level_array,door_list,current_level)
        
        if boss.next_attack_tick == MAX_TIME_TO_NEXT_ATTACK:
            boss.next_attack_tick = 0
            boss.attack(character,current_level)
        else:
            boss.next_attack_tick+=1

        

        for k in render_list:
            k.clear(DISPLAY_SURFACE,level_image)
        for i in boss.goon_list:
            i.clear(DISPLAY_SURFACE,level_image)
            if second_clock == 0:
                i.damage(character,current_level)
            i.pathfind(character.x,character.y,level_array,door_list,current_level)
        for i in boss.goon_list:
            i.render(current_level,DISPLAY_SURFACE)
        for l in button_list:
            button.Button.pressed(l,item_list)
        for m in door_list:
            door.Door.open(m,button_list)
        for i in render_list:
            i.render(current_level,DISPLAY_SURFACE)
        for j in enemie_list:
            if second_clock == 0:
                j.damage(character,current_level)
            j.pathfind(character.x,character.y,level_array,door_list,current_level)
        




screen_load.load_level("Level1",DISPLAY_SURFACE)

while True: # tady začíná hlavní herní loop
    screen_load.clear_bit(DISPLAY_SURFACE,level_image,0,0,200,200) #na reloading fps counteru
    player.Person.clear(character,DISPLAY_SURFACE,level_image)
    render_everything()
    animation_frame = player.Person.render(character,DISPLAY_SURFACE,direction,walking,animation_frame) # načte texturu hráče

    if character.health <= 0:
        print("\n\nZemřel jsi :(\n\n")
        pygame.quit()
        sys.exit()


    second_clock+=1
    if second_clock > 100:
        second_clock = 0

    time_delta = clock.tick(200)/1000 # časovač pro menu elementy
    for event in pygame.event.get(): #ovládání eventů
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

        else:
            if event.type == pygame.MOUSEBUTTONUP:
                for i in enemie_list:
                    i.is_touching_player(character.x,character.y,current_level)
                for i in boss.goon_list:
                    i.is_touching_player(character.x,character.y,current_level)
                sword_used = True
                boss.is_touching_player(character.x,character.y,current_level)
            
            
    
    if game_started == True:    # tento kód se spustí jen když už hrajete hru (když v menu vyberete že chcete hrát)
        if direction == RIGHT:
            rotation = sword_angle*-1
        elif direction == DOWN:
            rotation = sword_angle*-1+270
        elif direction == LEFT:
            rotation = sword_angle*-1+180
        elif direction == UP:
            rotation = sword_angle*-1+90

        if sword_animation_frame == SWORD_ANIMATION_LENGHT:
            sword_animation_frame=0
            sword_angle = 0
            sword_used = False
        if sword_used == True:
            DISPLAY_SURFACE.blit(pygame.transform.rotate(sword_texture,rotation),(character.x,character.y))
            sword_animation_frame+=1
            sword_angle+=90/SWORD_ANIMATION_LENGHT



        key_pressed_is = pygame.key.get_pressed() #kód na ovládání hráče
            # první 4 if jsou na úhlopříčky a ty další 4 na rovný směry

        if key_pressed_is[K_e]:
            for i in item_list:
                i.is_touching_player(character.x,character.y,character,current_level)
            
            
        
        diagonal_speed = (move_speed*two_sqrt)/2
        if key_pressed_is[K_w] and key_pressed_is[K_d] and not key_pressed_is[K_a] and not key_pressed_is[K_s]:
            player.Person.move_y(character,-(diagonal_speed),direction,door_list)
            player.Person.move_x(character,(diagonal_speed),direction,door_list)
            direction = RIGHT
            walking = True
            
        elif not key_pressed_is[K_w] and key_pressed_is[K_d] and not key_pressed_is[K_a] and key_pressed_is[K_s]:
            player.Person.move_y(character,(diagonal_speed),direction,door_list)
            player.Person.move_x(character,(diagonal_speed),direction,door_list)
            direction = RIGHT
            walking = True
                
            
        elif not key_pressed_is[K_w] and not key_pressed_is[K_d] and key_pressed_is[K_a] and key_pressed_is[K_s]:
            player.Person.move_y(character,(diagonal_speed),direction,door_list)
            player.Person.move_x(character,-(diagonal_speed),direction,door_list)
            direction = LEFT
            walking = True
                
            
        elif key_pressed_is[K_w] and not key_pressed_is[K_d] and key_pressed_is[K_a] and not key_pressed_is[K_s]:
            player.Person.move_y(character,-(diagonal_speed),direction,door_list)
            player.Person.move_x(character,-(diagonal_speed),direction,door_list)
            direction = LEFT
            walking = True
                
            
        elif key_pressed_is[K_w]:
            player.Person.move_y(character,-move_speed,direction,door_list)
            walking = True
            direction = UP
                
        elif key_pressed_is[K_a]:
            player.Person.move_x(character,-move_speed,direction,door_list)
            walking = True
            direction = LEFT
                
        elif key_pressed_is[K_s]:
            player.Person.move_y(character,move_speed,direction,door_list)
            walking = True
            direction = DOWN
                
        elif key_pressed_is[K_d]:
            player.Person.move_x(character,move_speed,direction,door_list)
            walking = True
            direction = RIGHT
                
        elif not key_pressed_is[K_d] and not key_pressed_is[K_a] and not key_pressed_is[K_s] and not key_pressed_is[K_w]:
            walking = False
                

        if player.Person.end_of_word(character,screen_X-16,screen_Y-16) != None: # ovládání screen wrappingu
            js = open("levels\level_conection.json")
            data = json.load(js)
            next_level = data[current_level]
            if player.Person.end_of_word(character,screen_X-16,screen_Y-16) == "Left":
                screen_load.load_level(next_level[LEFT]["Left"],DISPLAY_SURFACE)
                player.Person.set_x(character,int(data[current_level][LEFT]["X"]))
                player.Person.set_y(character,int(data[current_level][LEFT]["Y"]))
                current_level = next_level[LEFT]["Left"]
            elif player.Person.end_of_word(character,screen_X-16,screen_Y-16) == "Up":
                screen_load.load_level(next_level[UP]["Up"],DISPLAY_SURFACE)
                player.Person.set_x(character,int(data[current_level][UP]["X"]))
                player.Person.set_y(character,int(data[current_level][UP]["Y"]))
                current_level = next_level[UP]["Up"]
            elif player.Person.end_of_word(character,screen_X-16,screen_Y-16) == "Down":
                screen_load.load_level(next_level[DOWN]["Down"],DISPLAY_SURFACE)
                player.Person.set_x(character,int(data[current_level][DOWN]["X"]))
                player.Person.set_y(character,int(data[current_level][DOWN]["Y"]))
                current_level = next_level[DOWN]["Down"]
            elif player.Person.end_of_word(character,screen_X-16,screen_Y-16) == "Right":
                screen_load.load_level(next_level[RIGHT]["Right"],DISPLAY_SURFACE)
                player.Person.set_x(character,int(data[current_level][RIGHT]["X"]))
                player.Person.set_y(character,int(data[current_level][RIGHT]["Y"]))
                current_level = next_level[RIGHT]["Right"]

    if game_started == True: # tento kód se spustí jen když už hrajete hru (když v menu vyberete že chcete hrát)
        if loaded_level != current_level:
            loaded_level = current_level
            level_hitbox, level_image = screen_load.load_level(current_level,DISPLAY_SURFACE) # načte texturu levelu
            level_array = screen_load.load_level_array(level_hitbox)
        screen_load.Render_Text(str(int(clock.get_fps()))+ " FPS",(0,0,0),(0,0),DISPLAY_SURFACE)
        screen_load.Render_Health(character,DISPLAY_SURFACE,healthbar_texture,healthbar_pointer_texture)




    if game_started == False: # tento kód ovládá menu
        image = pygame.image.load(os.path.join('Graphics\Menu\Background.jpg'))
        manager.process_events(event)
        manager.update(time_delta)
        DISPLAY_SURFACE.blit(image,(0,0))
        manager.draw_ui(DISPLAY_SURFACE)

    pygame.display.update() # update obrazovky
    
