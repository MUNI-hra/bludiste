from turtle import right
import pygame, sys
import screen_load
from pygame.locals import *
import os
from PIL import Image,ImageOps
import a_star_pathfinding
import random
import button
import goon



MAX_TIME_TO_NEXT_ATTACK = 100
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
SIZE_OF_CHARACTER = 78
CLEAN_OFFSET = 2
CLEAN_SIZE = 82
REACTION_SPACE = 100



class Boss:
    def __init__(self,level,x,y):
        self.x = x
        self.y = y
        self.last_x = 0
        self.last_y = 0
        self.health = 50
        self.strenght = 7
        self.iq = 15
        self.speed = 0.25
        self.texture = pygame.image.load(os.path.join('Graphics\Boss\Boss.png'))
        self.current_level = level
        self.pathway = []
        self.direction = RIGHT
        self.walking = True
        self.died = False
        self.next_attack_tick = 0
        self.goon_list = []

    def pathfind(self,playerx,playery,level,door_list,current_level):
        if self.health >0:
            if self.current_level == current_level:
                start = (int(self.x/16), int(self.y/16))

                if int(self.x/16) + self.iq < int(playerx/16) or int(self.x/16) -self.iq > int(playerx/16) or int(self.y/16) + self.iq < int(playery/16) or int(self.y/16) -self.iq > int(playery/16):
                    self.move_x(random.randint(-1,1)*self.speed,self.direction,door_list)
                    self.move_y(random.randint(-1,1)*self.speed,self.direction,door_list)
                else:
                    end = (int(playerx/16), int(playery/16))
                    if len(self.pathway) == 0:
                        self.pathway = a_star_pathfinding.main(level,start,end)

                    else:
                        xway = self.pathway[0][0]
                        yway = self.pathway[0][1]

                        if xway > int(self.x/16) and yway > int(self.y/16):
                            self.move_x(self.speed,self.direction,door_list)
                            self.move_y(self.speed,self.direction,door_list)
                            self.direction = RIGHT
                        elif xway > int(self.x/16) and yway < int(self.y/16):
                            self.move_x(self.speed,self.direction,door_list)
                            self.move_y(-self.speed,self.direction,door_list)
                            self.direction = RIGHT
                        elif xway < int(self.x/16) and yway > int(self.y/16):
                            self.move_x(-self.speed,self.direction,door_list)
                            self.move_y(self.speed,self.direction,door_list)
                            self.direction = LEFT
                        elif xway < int(self.x/16) and yway < int(self.y/16):
                            self.move_x(-self.speed,self.direction,door_list)
                            self.move_y(-self.speed,self.direction,door_list)
                            self.direction = LEFT
                        
                        elif xway > int(self.x/16) and yway == int(self.y/16):
                            self.move_x(self.speed,self.direction,door_list)
                            self.direction = RIGHT

                        elif xway < int(self.x/16) and yway == int(self.y/16):
                            self.move_x(-self.speed,self.direction,door_list)
                            self.direction = LEFT

                        elif yway > int(self.y/16) and xway == int(self.x/16):
                            self.move_y(self.speed,self.direction,door_list)
                            self.direction = DOWN

                        elif yway < int(self.y/16) and xway == int(self.x/16):
                            self.move_y(-self.speed,self.direction,door_list)
                            self.direction = UP
                        
                        self.pathway.pop(0)
        else:
            print("\n\nGrtuluji, Vyhrál jsi :)\n\n")
            pygame.quit()
            sys.exit()
    
    def player_interacted(self,level):
        if level == self.current_level:
            self.health -=1
    
    def is_touching_player(self,xplayer,yplayer,level):
        if xplayer > self.x-REACTION_SPACE and xplayer < self.x+REACTION_SPACE:
            if yplayer > self.y-REACTION_SPACE and yplayer < self.y+REACTION_SPACE:
                Boss.player_interacted(self,level)
                return self
    
    def attack(self,player,level):
        if self.health > 0:
            if level == self.current_level:
                attack = random.randint(1,3)
                if attack == 1:
                    self.damage(player,level)
                elif attack == 2:
                    self.goon_list.append(goon.Goon("Level8",self.x,self.y,self))
                    self.goon_list.append(goon.Goon("Level8",self.x,self.y,self))
                    self.goon_list.append(goon.Goon("Level8",self.x,self.y,self))
                elif attack == 3:
                    d = []
                    x = random.randint(-400,400)
                    y = random.randint(-400,400)
                    if self.x+x > 1280 or self.x+x < 0 or self.y+y > 960 or self.y+y < 0 or self.x-x > 1280 or self.x-x < 0 or self.y-y > 960 or self.y-y < 0:
                        self.move_x(x,1,d)
                        self.move_y(y,1,d)
                if self.x > 1280 or self.x < 0 or self.y > 960 or self.y < 0:
                    self.set_x(640)
                    self.set_y(480)
            
    
    def damage(self,player,level):
        if self.health > 0:
            if player.x > self.x-REACTION_SPACE and player.x < self.x+REACTION_SPACE:
                if player.y > self.y-REACTION_SPACE and player.y < self.y+REACTION_SPACE:
                    if level == self.current_level:
                        if not player.health <= 0:
                            player.health -=self.strenght/3
            

    def move_y(self, ya,dir,door_list):
        wall = screen_load.hitbox_detection(self.x, (self.y+ya),dir,door_list)  # is there a wall?
        if wall == True:
            self.last_y = self.y
            self.y += ya  # moving on y
        elif wall == "Jump Up":
            self.last_y = self.y
            self.y -= 88
        elif wall == "Jump Down":
            self.last_y = self.y
            self.y += 48

    def move_x(self, xa,dir,door_list):
        wall = screen_load.hitbox_detection((self.x + xa), self.y,dir,door_list)  # is there a wall?
        if wall == True:
            self.last_x = self.x
            self.x += xa
        elif wall == "Jump Left":
            self.last_x = self.x
            self.x -= 88
        elif wall == "Jump Right":
            self.last_x = self.x
            self.x += 48  # moving on x
    
    def set_x(self, xpos): # nastaví x na pozici v absolutních souřadnicích
        self.x = xpos
        self.last_x = xpos
    
    def set_y(self, ypos): # nastaví y na pozici v absolutních souřadnicích
        self.y = ypos
        self.last_y = ypos

        
    def clear(self,surface,image):
        surface.blit(image, (self.last_x-CLEAN_OFFSET,self.last_y-CLEAN_OFFSET),(self.last_x-CLEAN_OFFSET,self.last_y-CLEAN_OFFSET,CLEAN_SIZE,CLEAN_SIZE))


    def render(self,current_level,display): # rendruje hráče 
        
        if self.health > 0:
            if current_level == self.current_level:
                if self.direction == RIGHT:
                    texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Boss\Boss.png')), True, False)
                else:
                    texture = pygame.image.load(os.path.join('Graphics\Boss\Boss.png'))

                display.blit(pygame.transform.scale(texture,(SIZE_OF_CHARACTER,SIZE_OF_CHARACTER)), (self.x,self.y))        

