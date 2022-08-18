import pygame
import pygame, sys
from pygame.locals import *
import random
import decimal
import time
import os

def main():
    pygame.init()

    (width,height) = (640,640)

    clock = pygame.time.Clock()

    DISPLAY = pygame.display.set_mode((width,height))

    black= (0,0,0)

    DISPLAY.fill(black)

    #pictures and spirtes

    DuckPic = pygame.image.load("Duck Sprite.jpg")
    DuckPic = pygame.transform.scale(DuckPic, (128, 72))

    BreadPic = pygame.image.load("breadpic.jpg")
    BreadPic = pygame.transform.scale(BreadPic, (128, 72))

    class Food(pygame.sprite.Sprite):
        def __init__(self, xpos,ypos):
            super().__init__()
            self.xpos = xpos
            self.ypos = ypos
            self.image = BreadPic
            self.rect = self.image.get_rect()

    FoodList = []

    for i in range (5):
        FoodList.append(Food(random.randint(0,640),random.randint(0,640)))
    
    class Duck(pygame.sprite.Sprite):
        def __init__(self,xpos,ypos,speed,hunger,movement):
            super().__init__()
            self.xpos = xpos
            self.ypos = ypos
            self.image = DuckPic
            self.rect = self.image.get_rect()
            self.speed = speed
            self.hunger = hunger
            self.movement = movement

    Ducks = []

    for i in range(5):
        Ducks.append(Duck(xpos = random.randint(0, 320), ypos = random.randint(0, 320), speed =(random.randint(1,3)), hunger = 1000, movement = random.randint(1,100)))



    #COUNTERS

    ###------------ GAME STUFF INSTANCES HAPPENING


 
    # If the objects are colliding
    # then changing the y coordinate



    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        

        #display screen then food then ducks
        DISPLAY.fill(black)

        breadxy = []

        for i,FoodItem, in enumerate(FoodList):
            DISPLAY.blit(FoodItem.image, (FoodItem.xpos, FoodItem.ypos))
            xytuple = tuple[FoodItem.xpos , FoodItem.ypos]
            breadxy.append(xytuple)
        
        

        for i,Ducky in enumerate(Ducks):
            DISPLAY.blit(Ducky.image, (Ducky.xpos, Ducky.ypos))

            wheretogo = random.randint(Ducky.movement,100)

            if wheretogo < 25 :
                Ducky.xpos += Ducky.speed  
            if wheretogo > 25 and wheretogo < 50:
                Ducky.xpos -= Ducky.speed  
            if wheretogo > 50 and wheretogo < 75:
                Ducky.ypos += Ducky.speed  
            if wheretogo > 75 and wheretogo < 100:
                Ducky.ypos -= Ducky.speed  

            Ducky.hunger = Ducky.hunger - 1*Ducky.speed
            #print(Ducky.hunger)
            if Ducky.hunger < 0:
                
                del Ducks[i]

            #check for collision thorugh list of all objects of duck
            for i in breadxy:
                if tuple[Ducky.xpos,Ducky.ypos] == i:
                    print(i)
                    print("hit")
            
        #make the screen
        pygame.display.update()
    
    
main()