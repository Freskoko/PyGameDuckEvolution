import pygame
import pygame, sys
from pygame.locals import *
import random
import math

def main():
    pygame.init()

    (width,height) = (640,640)

    clock = pygame.time.Clock()

    DISPLAY = pygame.display.set_mode((width,height))

    blue= (0,60,200)

    DISPLAY.fill(blue)

    #pictures and spirtes

    DuckPic = pygame.image.load("Duck Sprite.jpg").convert_alpha()
    DuckPic = pygame.transform.smoothscale( DuckPic, (128, 72))

    BreadPic = pygame.image.load("breadpic.jpg").convert_alpha()
    BreadPic = pygame.transform.smoothscale(BreadPic, (128, 72))

    class Food(pygame.sprite.Sprite):
        def __init__(self, xpos,ypos):
            super().__init__()
            self.image = BreadPic
            self.rect = self.image.get_rect()
            self.rect.topleft = ( xpos, ypos )
            self.eaten = False

        def eat( self, ate=True ):
            self.eaten = ate

        def __str__( self ):
            value = "Food at (%d,%d)" % ( self.rect.x, self.rect.y )
            if ( self.eaten ):
                value += " (eaten)"
            return value
                

    FoodList = []
    for i in range (10):
        FoodList.append(Food(random.randint(30,600),random.randint(30,600)))
    
    class Duck(pygame.sprite.Sprite):
        def __init__(self,xpos,ypos,speed,hunger,movement):
            super().__init__()
            self.image = DuckPic
            self.rect = self.image.get_rect()
            self.rect.topleft = ( xpos, ypos )
            self.speed = speed
            self.hunger = hunger
            self.movement = movement

        def distanceTo( self, bread_sprite ):
            """ Calculate the distance from us to a FoodItem """
            duck_x, duck_y   = self.rect.center
            bread_x, bread_y = bread_sprite.rect.center
            # ref: https://en.wikipedia.org/wiki/Euclidean_distance
            x_part = ( bread_x - duck_x )
            y_part = ( bread_y - duck_y )
            distance = math.sqrt( ( x_part * x_part ) + ( y_part * y_part ) )
            return distance

        def __str__( self ):
            return "Duck at (%d,%d)" % ( self.rect.x, self.rect.y )


    Ducks = []

    for i in range(1):
        Ducks.append(Duck(xpos = random.randint(0, 320), ypos = random.randint(0, 320), speed =(random.randint(1,3)), hunger = 1000, movement = random.randint(1,100)))


    ###------------ GAME STUFF INSTANCES HAPPENING

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if FoodList == []:
            print("ducks ate all the bread")
            pygame.quit()
            sys.exit()

        if Ducks == []:
            print("all ducks died")
            pygame.quit()
            sys.exit()
        

        #display screen then food then ducks
        DISPLAY.fill(blue)

        
        for i,Ducky in enumerate(Ducks):

            closestlist = [] #reset list of closest breads for all ducks

            for bread in enumerate(FoodList):
               
                closestlist.append([ Ducky.distanceTo( bread ), bread ] )

                closestlist.sort( key=lambda x : x[0] )  # sort by distance
                closest_bread_distance, closest_bread = closestlist[0]

                #closest list shows a value of how close a duck is to the bread 
                #where 0 or -1 = best score 
            
            #print(f"I'm moving to bread {indexofBread} with value of {max(closestlist)} which is at {FoodList[indexofBread].xpos,FoodList[indexofBread].ypos}, my postion is {Ducky.xpos, Ducky.ypos} other values include = {closestlist}")

            if True:
            #move duck to closest bread
                if Ducky.xpos < closest_bread.rect.x:
                    Ducky.xpos += 1 * Ducky.speed
                    
                if Ducky.xpos > closest_bread.rect.x:
                    Ducky.xpos -= 1 * Ducky.speed

                if Ducky.ypos > closest_bread.rect.y:
                    Ducky.ypos -= 1 * Ducky.speed   

                if Ducky.ypos< closest_bread.rect.y:
                    Ducky.ypos += 1 * Ducky.speed            

            Ducky.hunger = Ducky.hunger - 1*Ducky.speed
            #duck hunger goes down, faster duck looses more hunger

            if Ducky.hunger < 0: #if duck at 0 hunger he dies :(
                del Ducks[i]


            #display the bread

            #check for distabce to bread, so check if distance is rly low
            breads_to_add = 0
            for distance, bread in closestlist:
                if ( distance < 5 ):    # pixels
                    bread.eat()
                    breads_to_add += 1
                    Ducky.hunger += 60

            if ( breads_to_add > 0 ):
                print( "ATE %d BREADS" % ( breads_to_add ) )
                # remove the eaten breads
                FoodList = [ b for b in FoodList if ( not b.eaten ) ]

            # add some new bread
            for i in range( breads_to_add ):
                FoodList.append(Food(random.randint(30,600),random.randint(30,600)))
                
                    
            for FoodItem in (FoodList):
            
                DISPLAY.blit(FoodItem.image, (FoodItem.xpos, FoodItem.ypos))

            #DISPLAY DUCK

            DISPLAY.blit(Ducky.image, (Ducky.xpos, Ducky.ypos))
        
        pygame.display.update()
            
        #make the screen
        
    
    
main()