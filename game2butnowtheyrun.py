import pygame
import pygame, sys
from pygame.locals import *
import math
import random
import time
import matplotlib.pyplot as plt

#TODOO = FIX CRASH WHEN WOLFVES ARE ALL DEAD AND TRY TO DRAW GRAPH

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

    #ducks/bread/foxes to spawn initially
    ducksPerGeneration = 30
    BreadPerGeneration = 70
    AmountOfFoxes = 6
    
    minbreaddistance = 15 #how close does a duck need to be to eat a bread

    breadeatreward = 300 #how much reward for eating a bread (max hunger == 1000 then he is not hungry anymore)
    duckeatreward = 500
   
    penaltyformoving = 0.95 #the moving penalty (is muliplied with speed)
    penaltyformovingFox = 0.65 #the moving penalty (is muliplied with speed)

    minhungertoreproduce = 600 #minium hunger to reproduce (you cant reproduce if you are almost dead)

    timetoevolve = 300 #how much time should be between each eovlution sequence
    timetoevolveFox = 600

    timecounter = 0 #do not change, initial setting of time
    timecounterFox = 0 #do not change used for fox evolution 
    timecounterGlobal = 0 #used for graph do not change
    ducksandspeedlist = [] #used for graph
    timecounterList = []
    howmanyduckslist = [] #used for graph
    howmanyFoxeslist = [] #used for graph
    duckspeedmulitplierForList = 10 # used to add to graph 
    foxspeedmulitplierforlist = 10
    MegaFoxSpeedList = []

    IMAGESIZE = 25

    #---------------------------------------------------------------------------


    #text and font

    pygame.font.init() 
    my_font = pygame.font.SysFont('Comic Sans MS', 15)

    #pics

    DuckPic = pygame.image.load("Duck Sprite.jpg").convert_alpha()
    DuckPic = pygame.transform.smoothscale( DuckPic, (IMAGESIZE, IMAGESIZE))

    BreadPic = pygame.image.load("breadpic.jpg").convert_alpha()
    BreadPic = pygame.transform.smoothscale(BreadPic, (IMAGESIZE, IMAGESIZE))

    FoxPic = pygame.image.load("foxpic.jpg").convert_alpha()
    FoxPic = pygame.transform.smoothscale(FoxPic, (45, 45))  

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
        def __init__(self,xpos,ypos,speed,hunger,scaredness):
            super().__init__()
            self.image = DuckPic
            self.rect = self.image.get_rect()
            self.rect.topleft = ( xpos, ypos )
            self.speed = speed
            self.hunger = hunger
            self.scaredness = scaredness
            self.eaten = False

        def distanceTo( self, bread_sprite ):
            """ Calculate the distance from us to a FoodItem """
            duck_x, duck_y   = self.rect.center
            bread_x, bread_y = bread_sprite.rect.center

            #https://en.wikipedia.org/wiki/Euclidean_distance

            x_part = ( bread_x - duck_x )
            y_part = ( bread_y - duck_y )

            distance = math.sqrt( ( x_part * x_part ) + ( y_part * y_part ) )
            return distance

        def eat( self, ate=True ):
            self.eaten = ate

        def __str__( self ):
            value = "Food at (%d,%d)" % ( self.rect.x, self.rect.y )
            if ( self.eaten ):
                value += " (eaten)"
            return value

    class Fox(pygame.sprite.Sprite):
        def __init__(self,xpos,ypos,speed,hunger,scaredness):
            super().__init__()
            self.image = FoxPic
            self.rect = self.image.get_rect()
            self.rect.topleft = ( xpos, ypos )
            self.speed = speed
            self.hunger = hunger
            self.scaredness = scaredness

        def distanceTo( self, other_thing ):
            """ Calculate the distance from us to something else """
            fox_x, fox_y   = self.rect.center
            otherthingx, otherthingy = other_thing.rect.center

            #https://en.wikipedia.org/wiki/Euclidean_distance

            x_part = ( otherthingx - fox_x )
            y_part = ( otherthingy - fox_y )

            distance = math.sqrt( ( x_part * x_part ) + ( y_part * y_part ) )
            return distance

        def __str__( self ):
            return "Fox at (%d,%d)" % ( self.rect.x, self.rect.y )

    class notEnoughGenes(Exception):
       pass

    #make the ducks and food and foxes
    Ducks = []

    for i in range(ducksPerGeneration):
        Ducks.append(Duck(xpos = random.randint(minxy, maxx), ypos = random.randint(minxy, maxy), speed =(random.randint(1,8)), hunger = 2000, scaredness = random.randint(100,300)))

    FoodList = []

    for i in range (BreadPerGeneration):
        FoodList.append(Food(random.randint(30,600),random.randint(30,600)))

    Foxes = []

    for i in range (AmountOfFoxes):
        Foxes.append(Fox(xpos = random.randint(minxy, maxx), ypos = random.randint(minxy, maxy), speed =(random.randint(3,5)), hunger = 5000, scaredness = random.randint(1,100)))

    #defining evolution and its propteries

    def evolve(OrganismList,ClassType,AttributeToEvolve):

        genePool = [] #acts as the gene pool for speed

        for organism in OrganismList:
            if organism.hunger > minhungertoreproduce: #must not be too hungry to pass on genes #set to 100 usually
                if getattr(organism, AttributeToEvolve) != 0: #cannot reprodce if its 0
                    genePool.append(getattr(organism, AttributeToEvolve)) #add to gene pool

        if len(genePool) < 2:
            raise notEnoughGenes

        if len(genePool) >= 2:

            newAttributeList = []

            genecounter = 0

            for j in range(int(len(genePool)/2)):

                GeneForNewAttribute = (genePool[genecounter] + genePool[genecounter+1])/2

                #example ==== duckspeedlist = [1,3] where 1 and 3 are speeds which have managed to reproduce
                #then we take the average of those two genes and add mutation (slowerorfaster)

                #duckspeedlist may actually look like = [1,3,4,5,1,3,4,5,6,6] where then genes
                #1,3 and  4,5 and 1,3 etc combine, but there will form trends. 

                newAttributeList .append(GeneForNewAttribute)

                genecounter += 2
                
            for gene in newAttributeList : #here we add a new duck to the game, so here more mutations can take place
                randomUpOrDown = 0 #assign 

                if gene < 1:
                    randomUpOrDown = 0 #negative speed is bad
                    gene = 1
                if gene > 1:
                    randomUpOrDown = random.randint(-2,2) #mutation

                OrganismList.append(ClassType(xpos = random.randint(minxy, maxx), ypos = random.randint(minxy, maxy), speed =(gene+ randomUpOrDown), hunger = 1000, scaredness = random.randint(30,100)))
            print("evolution success!")
            print(timecounter)

        #reset time to evolve after evolution 

    def show_data():

        fig, ax = plt.subplots()

        plt.plot(timecounterList, ducksandspeedlist,"r-", label="AVG Duck Speed * 10")
        plt.plot(timecounterList, MegaFoxSpeedList,"b-", label="AVG Fox Speed * 10")
        plt.plot(timecounterList,howmanyduckslist,"c-", label="Amount of ducks")
        plt.plot(timecounterList,howmanyFoxeslist,"m-", label="Amount of foxes")
        
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
        timecounterFox += 1
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

        for i,FoxGuy in enumerate(Foxes):
            closestducklist = [] #reset list of closest breads for all ducks
            for ducky in Ducks:
                # Made a list of ducks & their distance

                closestducklist.append( [ FoxGuy.distanceTo( ducky ), ducky ] )

                closestducklist.sort( key=lambda x : x[0] )  # sort by distance
                closest_bread_distance, closest_bread = closestducklist[0]

            if True:
            #move fox to closest bread
                if FoxGuy.rect.x < closest_bread.rect.x:
                    FoxGuy.rect.x += 1 * FoxGuy.speed
                    
                if FoxGuy.rect.x > closest_bread.rect.x:
                    FoxGuy.rect.x -= 1 * FoxGuy.speed

                if FoxGuy.rect.y > closest_bread.rect.y:
                    FoxGuy.rect.y -= 1 * FoxGuy.speed   

                if FoxGuy.rect.y < closest_bread.rect.y: 
                    FoxGuy.rect.y += 1 * FoxGuy.speed            

            FoxGuy.hunger = FoxGuy.hunger - (penaltyformovingFox * FoxGuy.speed) #FoxGuy hunger goes down, faster duck looses more hunger
            if FoxGuy.speed <= 0:
                FoxGuy.hunger -= 1000 #incase duck has 0 speed

            if FoxGuy.hunger < 0: #if duck at 0 hunger he dies :(
                del Foxes[i]

            # if distance to duck is low, FoxGuy eats it
            
            for distance, ducky in closestducklist:
                if ( distance < minbreaddistance ):    # pixels #this is also min bread distance but we use same for fox
                    print( "EATING DUCKY" )
                    ducky.eat()
                    
                    if FoxGuy.hunger < 5000:
                        FoxGuy.hunger += duckeatreward #REWARD FOR EATING DUCK
                    
                    #this is supposed to be ducks 
                    if ( len(Ducks) > 0 ):
                        #print( "ATE %d BREADS" % ( breads_to_add ) )
                        # remove the eaten breads
                        Ducks = [ d for d in Ducks if ( not d.eaten ) ]


        for i,Ducky in enumerate(Ducks):

            runaway = False

            #scaredness make them run away from fox!

            #FOX DETECTION BELOW -----------------
            closestFoxlist = [] #reset list of closest fox for all ducks

            for Foxy in Foxes:
                # Made a list of fox & their distance

                closestFoxlist.append( [ Ducky.distanceTo( Foxy ), Foxy ] )

                closestFoxlist.sort( key=lambda x : x[0] )  # sort by distance
                closest_fox_distance, closest_fox = closestFoxlist[0]

            if closest_fox_distance < Ducky.scaredness:
                runaway = True

            if runaway == True:
            #move duck away from closest fox
                if Ducky.rect.x < closest_fox.rect.x:
                    Ducky.rect.x -= 1 * Ducky.speed
                    
                if Ducky.rect.x > closest_fox.rect.x:
                    Ducky.rect.x += 1 * Ducky.speed

                if Ducky.rect.y > closest_fox.rect.y:
                    Ducky.rect.y += 1 * Ducky.speed   

                if Ducky.rect.y < closest_fox.rect.y: 
                    Ducky.rect.y -= 1 * Ducky.speed  

                #out of bounds
                if Ducky.rect.x < minxy:
                    Ducky.rect.x -= 1 * Ducky.speed
                if Ducky.rect.x > maxx:
                    Ducky.rect.x += 1 * Ducky.speed   

                if Ducky.rect.y < minxy:
                    Ducky.rect.y += 1 * Ducky.speed  
                if Ducky.rect.y > maxy:
                    Ducky.rect.y -= 1 * Ducky.speed           

            Ducky.hunger = Ducky.hunger - (penaltyformoving * Ducky.speed) #duck hunger goes down, faster duck looses more hunger
            if Ducky.speed <= 0:
                Ducky.hunger -= 1000 #incase duck has 0 speed

            #BREAD DETECTION BELOW -----------------

            if runaway == False: #if fox is close then fuck no run away dont chase bread otherwise

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

                    #out of bounds
                    if Ducky.rect.x < minxy:
                        Ducky.rect.x = minxy + 1
                    if Ducky.rect.x > maxx:
                        Ducky.rect.x = maxx - 1     

                    if Ducky.rect.y < minxy:
                        Ducky.rect.y = minxy + 1
                    if Ducky.rect.y > maxy:
                        Ducky.rect.y = maxy - 1   

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
                        if Ducky.hunger < 3000:
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

        FoxSpeedlist = []
        #paint the fox 
        for FoxGuy in (Foxes):
            DISPLAY.blit(FoxGuy.image, (FoxGuy.rect.topleft))

            FoxSpeedlist.append(FoxGuy.speed)

        if len(Foxes) != 0:
            howmanyFoxeslist.append(len(Foxes))

            MegaFoxSpeedList.append( (sum(FoxSpeedlist) / len(FoxSpeedlist))*foxspeedmulitplierforlist)



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
                #def evolve(OrganismList,ClassType):
                evolve(Ducks,Duck,"speed")
                timecounter = 0
            except notEnoughGenes:
                pass

        if timecounterFox > timetoevolveFox:
            try:
                #def evolve(OrganismList,ClassType):
                evolve(Foxes,Fox,"speed")
                timecounterFox = 0
            except notEnoughGenes:
                pass

            #after evolution timecounter is set to 0 since we need to wait for time to evolve again
        if len(Ducks) < 2:
            print(len(Ducks))
            print("not enough ducks made it to reproduce --------- :(")
            show_data()
            pygame.quit()
            sys.exit()

        events = pygame.event.get() #this spacebar pause thing does not work
        for event in events:
            if event.type == pygame.K_SPACE:
                pygame.time.wait(10000) 
        
        pygame.display.update()
            
        
main()

