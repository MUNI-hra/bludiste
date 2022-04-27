import pygame, sys
import screen_load
from pygame.locals import *
import os
from PIL import Image,ImageOps
import a_star_pathfinding
import random


MAX_ANIMATION_FRAME = 100 # kolik snímků má animace (1 snímek je 1/20 sekundy)
END_OF_FRAME = 50
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
SIZE_OF_CHARACTER = 32
CLEAN_OFFSET = 2
CLEAN_SIZE = 36
REACTION_SPACE = 24



class Enemy:
    def __init__(self,level,x,y):
        self.x = x
        self.y = y
        self.last_x = 0
        self.last_y = 0
        self.health = random.randint(1,5)
        self.strenght = random.randint(1,3)
        self.iq = random.randint(5,20)
        self.speed = random.randint(40,80)/100
        self.texture = pygame.image.load(os.path.join('Graphics\Enemie\Front.png'))
        self.current_level = level
        self.pathway = []
        self.direction = RIGHT
        self.animation_frame = 0
        self.walking = True
        self.color = random.randint(0,36)*10

    def pathfind(self,playerx,playery,level):
        if self.health >0:
            start = (int(self.x/16), int(self.y/16))

            if int(self.x/16) + self.iq < int(playerx/16) or int(self.x/16) -self.iq > int(playerx/16) or int(self.y/16) + self.iq < int(playery/16) or int(self.y/16) -self.iq > int(playery/16):
                self.move_x(random.randint(-1,1)*self.speed,self.direction)
                self.move_y(random.randint(-1,1)*self.speed,self.direction)
            else:
                end = (int(playerx/16), int(playery/16))
                if len(self.pathway) == 0:
                    self.pathway = a_star_pathfinding.main(level,start,end)

                else:
                    xway = self.pathway[0][0]
                    yway = self.pathway[0][1]

                    if xway > int(self.x/16) and yway > int(self.y/16):
                        self.move_x(self.speed,self.direction)
                        self.move_y(self.speed,self.direction)
                        self.direction = RIGHT
                    elif xway > int(self.x/16) and yway < int(self.y/16):
                        self.move_x(self.speed,self.direction)
                        self.move_y(-self.speed,self.direction)
                        self.direction = RIGHT
                    elif xway < int(self.x/16) and yway > int(self.y/16):
                        self.move_x(-self.speed,self.direction)
                        self.move_y(self.speed,self.direction)
                        self.direction = LEFT
                    elif xway < int(self.x/16) and yway < int(self.y/16):
                        self.move_x(-self.speed,self.direction)
                        self.move_y(-self.speed,self.direction)
                        self.direction = LEFT
                    
                    elif xway > int(self.x/16) and yway == int(self.y/16):
                        self.move_x(-self.speed,self.direction)
                        self.direction = RIGHT

                    elif xway < int(self.x/16) and yway == int(self.y/16):
                        self.move_x(-self.speed,self.direction)
                        self.direction = LEFT

                    elif yway > int(self.y/16) and xway == int(self.x/16):
                        self.move_y(self.speed,self.direction)
                        self.direction = DOWN

                    elif yway < int(self.y/16) and xway == int(self.x/16):
                        self.move_y(-self.speed,self.direction)
                        self.direction = UP
                    
                    self.pathway.pop(0)
    
    def player_interacted(self,level):
        if level == self.current_level:
            self.health -=1
    
    def is_touching_player(self,xplayer,yplayer,level):
        if xplayer > self.x-REACTION_SPACE and xplayer < self.x+REACTION_SPACE:
            if yplayer > self.y-REACTION_SPACE and yplayer < self.y+REACTION_SPACE:
                Enemy.player_interacted(self,level)
                return self
    
    def damage(self,player,level):
        if self.health > 0:
            if player.x > self.x-REACTION_SPACE and player.x < self.x+REACTION_SPACE:
                if player.y > self.y-REACTION_SPACE and player.y < self.y+REACTION_SPACE:
                    if level == self.current_level:
                        if not player.health <= 0:
                            player.health -=self.strenght/10


    def move_y(self, ya,dir):
        wall = screen_load.hitbox_detection(self.x, (self.y+ya),dir)  # is there a wall?
        if wall == True:
            self.last_y = self.y
            self.y += ya  # moving on y
        elif wall == "Jump Up":
            self.last_y = self.y
            self.y -= 88
        elif wall == "Jump Down":
            self.last_y = self.y
            self.y += 48

    def move_x(self, xa,dir):
        wall = screen_load.hitbox_detection((self.x + xa), self.y,dir)  # is there a wall?
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
                self.animation_frame +=1
                if self.animation_frame == MAX_ANIMATION_FRAME:
                    self.animation_frame = 0

    
                if self.direction == RIGHT: # rendering player if he is facing right 
                    if self.walking == True: # rendering animation of him walking
                        if self.animation_frame <= END_OF_FRAME:
                            texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Enemie\side_walk.png')), True, False)
                        if self.animation_frame > END_OF_FRAME:
                            texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Enemie\side.png')), True, False)
                    if self.walking == False: #rendering Enemie if he is not moving
                        texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Enemie\side.png')), True, False)

                elif self.direction == UP: # rendering Enemie if he is facing up
                    if self.walking == True: # rendering animation of him walking
                        if self.animation_frame <= END_OF_FRAME:
                            texture = pygame.image.load(os.path.join('Graphics\Enemie\Back_walk.png'))
                        if self.animation_frame > END_OF_FRAME:
                            texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Enemie\Back_walk.png')), True, False)
                    if self.walking == False:
                        texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Enemie\Back.png')), True, False)



                elif self.direction == LEFT: # rendering Enemie if he is facing left
                    if self.walking == True: # rendering animation of him walking
                        if self.animation_frame <= END_OF_FRAME:
                            texture = pygame.image.load(os.path.join('Graphics\Enemie\side_walk.png'))
                        if self.animation_frame > END_OF_FRAME:
                            texture = pygame.image.load(os.path.join('Graphics\Enemie\side.png'))
                    if self.walking == False: #rendering Enemie if he is not moving
                        texture = pygame.image.load(os.path.join('Graphics\Enemie\side.png'))



                elif self.direction == DOWN: # rendering Enemie if he is facing down 
                    if self.walking == True: # rendering animation of him walking
                        if self.animation_frame <= END_OF_FRAME:
                            texture = pygame.transform.flip(pygame.image.load(os.path.join('Graphics\Enemie\Front_walk.png')), True, False)
                        if self.animation_frame > END_OF_FRAME:
                            texture = pygame.image.load(os.path.join('Graphics\Enemie\Front_walk.png'))
                    if self.walking == False: #rendering Enemie if he is not moving
                        texture = pygame.image.load(os.path.join('Graphics\Enemie\Front.png'))




                display.blit(pygame.transform.scale(self.shift_color(texture),(SIZE_OF_CHARACTER,SIZE_OF_CHARACTER)), (self.x,self.y))        


    def shift_color(self,surface):
        # Get the pixels
        pixels = pygame.PixelArray(surface)
        # Iterate over every pixel                                             
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                # Turn the pixel data into an RGB tuple
                rgb = surface.unmap_rgb(pixels[x][y])
                # Get a new color object using the RGB tuple and convert to HSLA
                color = Color(*rgb)
                h, s, l, a = color.hsla
                # Add 120 to the hue (or however much you want) and wrap to under 360
                color.hsla = (int(h) + self.color) % 360, int(s), int(l), int(a)
                # Assign directly to the pixel
                pixels[x][y] = color
        # The old way of closing a PixelArray object
        del pixels
        return surface