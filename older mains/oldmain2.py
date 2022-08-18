import pygame
import pygame, sys
from pygame.locals import *
import math
import random
import time
import matplotlib.pyplot as plt


def main():

    #todo = add ghraph ppopulation, stop doing 0 speed

    pygame.init()
    
    (width,height) = (1280,1000)
    minxy = 0
    maxx = width
    maxy = height

    clock = pygame.time.Clock()

    #WINDOW SIZE:

    DISPLAY = pygame.display.set_mode((width,height))

    blue= (0,60,200)

    DISPLAY.fill(blue)


    #CONSTANTS CHANGE HERE -----------------------------

    #ducks/bread to spawn initially
    ducksPerGeneration = 5
    BreadPerGeneration = 35
    
    minbreaddistance = 15 #how close does a duck need to be to eat a bread

    breadeatreward = 170 #how much reward for eating a bread (max hunger == 1000 then he is not hungry anymore)
   
    penaltyformoving = 0.95 #the moving penalty (is muliplied with speed)

    minhungertoreproduce = 700 #minium hunger to reproduce (you cant reproduce if you are almost dead)

    timetoevolve = 700 #how much time should be between each eovlution sequence

    timecounter = 0 #do not change, initial setting of time
    timecounterGlobal = 0 #used for graph do not change
    ducksandspeedlist = [] #used for graph
    timecounterList = []
    howmanyduckslist = [] #used for graph
    duckspeedmulitplierForList = 10 # used to add to graph 


    #---------------------------------------------------------------------------


    #text and font

    pygame.font.init() 
    my_font = pygame.font.SysFont('Comic Sans MS', 15)

    #pics

    DuckPic = pygame.image.load("Duck Sprite.jpg").convert_alpha()
    DuckPic = pygame.transform.smoothscale( DuckPic, (25, 25))

    BreadPic = pygame.image.load("breadpic.jpg").convert_alpha()
    BreadPic = pygame.transform.smoothscale(BreadPic, (25, 25))

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

            #https://en.wikipedia.org/wiki/Euclidean_distance

            x_part = ( bread_x - duck_x )
            y_part = ( bread_y - duck_y )

            distance = math.sqrt( ( x_part * x_part ) + ( y_part * y_part ) )
            return distance

        def __str__( self ):
            return "Duck at (%d,%d)" % ( self.rect.x, self.rect.y )

    class notEnoughGenes(Exception):
       pass

    #make the ducks and food
    Ducks = []

    for i in range(ducksPerGeneration):
        Ducks.append(Duck(xpos = random.randint(minxy, maxx), ypos = random.randint(minxy, maxy), speed =(random.randint(2,8)), hunger = 1000, movement = random.randint(1,100)))

    FoodList = []

    for i in range (BreadPerGeneration):
        FoodList.append(Food(random.randint(30,600),random.randint(30,600)))

    #defining evolution and its propteries

    def evolve():

        duckspeedlist = [] #acts as the gene pool for speed

        for duck in Ducks:
            if duck.hunger > minhungertoreproduce: #must not be too hungry to pass on genes #set to 100 usually
                if duck.speed != 0: #cannot reprodce if you cant move 
                    duckspeedlist.append(duck.speed) #add to gene pool

        if len(duckspeedlist) < 2:
            raise notEnoughGenes

        if len(duckspeedlist) >= 2:

            newspeedlist = []

            genecounter = 0

            for j in range(int(len(duckspeedlist)/2)):

                GeneForNewSpeed = (duckspeedlist[genecounter] + duckspeedlist[genecounter+1])/2

                #example ==== duckspeedlist = [1,3] where 1 and 3 are speeds which have managed to reproduce
                #then we take the average of those two genes and add mutation (slowerorfaster)

                #duckspeedlist may actually look like = [1,3,4,5,1,3,4,5,6,6] where then genes
                #1,3 and  4,5 and 1,3 etc combine, but there will form trends. 

                newspeedlist.append(GeneForNewSpeed)

                genecounter += 2
                
            for gene in newspeedlist: #here we add a new duck to the game, so here more mutations can take place
                slowerorfaster = 0 #assign 

                if gene < 1:
                    slowerorfaster = 0 #negative speed is bad
                    gene = 1
                if gene > 1:
                    slowerorfaster = random.randint(-2,2) #mutation

                Ducks.append(Duck(xpos = random.randint(minxy, maxx), ypos = random.randint(minxy, maxy), speed =(gene+ slowerorfaster), hunger = 1000, movement = random.randint(1,100)))
            print("evolution success!")
            print(timecounter)

        #reset time to evolve after evolution 

    def show_data():

        fig, ax = plt.subplots()

        plt.plot(timecounterList, ducksandspeedlist,"r-", label="Speed")
        plt.plot(timecounterList,howmanyduckslist,"c-", label="Amount of ducks")

        ax.legend()

        plt.ylabel("speed")
        plt.xlabel("time")

        #plt.grid(True)

        plt.savefig("duckdata.png")
        plt.show()

    ###------------ GAME STUFF INSTANCES HAPPENING

    while True:
        clock.tick(60)

        timecounter += 1
        timecounterGlobal += 1
        #print(timecounterGlobal)

        for event in pygame.event.get():
            if event.type == QUIT:
                
                pygame.quit()
                show_data()
                sys.exit()
                

        if FoodList == []:
            print("ducks ate all the bread")
            pygame.quit()
            sys.exit()

        if Ducks == []:
            print("all ducks died")
            pygame.quit()
            sys.exit()
        

        for i,Ducky in enumerate(Ducks):

            closestlist = [] #reset list of closest breads for all ducks
            for bread in FoodList:
                # Made a list of breads & their distance
                closestlist.append( [ Ducky.distanceTo( bread ), bread ] )

                closestlist.sort( key=lambda x : x[0] )  # sort by distance
                closest_bread_distance, closest_bread = closestlist[0]

            if True:
            #move duck to closest bread
                if Ducky.rect.x < closest_bread.rect.x:
                    Ducky.rect.x += 1 * Ducky.speed
                    
                if Ducky.rect.x > closest_bread.rect.x:
                    Ducky.rect.x -= 1 * Ducky.speed

                if Ducky.rect.y > closest_bread.rect.y:
                    Ducky.rect.y -= 1 * Ducky.speed   

                if Ducky.rect.y < closest_bread.rect.y: 
                    Ducky.rect.y += 1 * Ducky.speed            

            Ducky.hunger = Ducky.hunger - (penaltyformoving * Ducky.speed) #duck hunger goes down, faster duck looses more hunger
            if Ducky.speed <= 0:
                Ducky.hunger -= 1000 #incase duck has 0 speed

            if Ducky.hunger < 0: #if duck at 0 hunger he dies :(
                del Ducks[i]

            #display the bread


            # if distance to bread is low, duck eats it
            breads_to_add = 0
            for distance, bread in closestlist:
                if ( distance < minbreaddistance ):    # pixels
                    #print( "EATING BREAD" )
                    bread.eat()
                    breads_to_add += 1
                    if Ducky.hunger < 2000:
                        Ducky.hunger += breadeatreward #REWARD FOR EATING BREAD
                        #print(Ducky.hunger)
                    
            if ( breads_to_add > 0 ):
                #print( "ATE %d BREADS" % ( breads_to_add ) )
                # remove the eaten breads
                FoodList = [ b for b in FoodList if ( not b.eaten ) ]

            # add some new bread
            for i in range( breads_to_add ):
                FoodList.append(Food(random.randint(minxy,maxx),random.randint(minxy,maxy)))
                        
            #print(Ducky.hunger)


        #make the screen

        #display screen then food then ducks
        # fill the background
        DISPLAY.fill(blue)

        # paint the bread
        for FoodItem in (FoodList):
            DISPLAY.blit(FoodItem.image, (FoodItem.rect.topleft))

        # paint the duck

        duckspeedlist = []
        
        for Ducky in Ducks:
            text_surface = my_font.render(f"{int(Ducky.hunger)}", False, (0, 0, 0))
            
            DISPLAY.blit(Ducky.image, (Ducky.rect.topleft))
            DISPLAY.blit(text_surface, (Ducky.rect.topleft))

            duckspeedlist.append(Ducky.speed)
        if len(duckspeedlist) != 0:
            ducksandspeedlist.append( (sum(duckspeedlist) / len(duckspeedlist))*duckspeedmulitplierForList )
            howmanyduckslist.append(len(duckspeedlist))
        timecounterList.append(timecounterGlobal)
            

        #paiunt the text saying average speed

        if len(duckspeedlist) != 0:
            SPEEDTEXT = my_font.render((f"average speed of duck = {round(sum(duckspeedlist) / len(duckspeedlist),1)}"), False, (0, 0, 0))


        #why is this onlyu adding once????
        

        DISPLAY.blit(SPEEDTEXT, (0,0))

        if timecounter > timetoevolve:
            try:
                
                evolve()
                timecounter = 0

            except notEnoughGenes:
                pass


            #after evolution timecounter is set to 0 since we need to wait for time to evolve again
        if len(Ducks) < 2:
            print(len(Ducks))
            print("not enough ducks made it to reproduce :(")
            show_data()
            pygame.quit()
            sys.exit()

        events = pygame.event.get() #this spacebar pause thing does not work
        for event in events:
            if event.type == pygame.K_SPACE:
                pygame.time.wait(10000) 
        
        pygame.display.update()
            
        
main()

