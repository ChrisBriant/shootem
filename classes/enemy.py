from include import get_file_path
from .collidables import Collidable
from .projectiles import EnemyProjectileLeft
import pygame, os


class Rocket(Collidable):

    def __init__(self, posx, posy, width, height):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.launchcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable = True

        #load images
        self.frames = [pygame.image.load(get_file_path("i","rocket" + "/rocket" + str(n) + ".png")) for n in range(5)]

        self.image.blit(self.frames[0], (0,0))

    """
    def draw(self,view):
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

        self.move()
        if self.walkCount + 1 >= 9:
            self.walkCount = 0

        if self.vel > 0:
            self.image.blit(self.walkRight[self.walkCount], (0,0))
            self.walkCount +=1
        else:
            self.image.blit(self.walkLeft[self.walkCount], (0,0))
            self.walkCount +=1
        view.blit(self.image,(self.rect.x,self.rect.y))
        #self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        #self.myhitbox = pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        """

    def draw(self,view):
        print("Drawing")
        self.draw(view)

    def move(self,**kwargs):
        self.launchcounter += 1
        if self.launchcounter > 30:
            if self.launchcounter - 30 < 5:
                #animage the launch
                self.image.blit(self.frames[self.launchcounter-30], (0,0))
            self.rect.y -= self.vel

    #Animate the explosion
    def hit(self, hitval):
        pass


class Scobot(Collidable):
    def __init__(self, posx, posy, width, height, movingdown):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.movingdown=movingdown
        self.destructable=True
        self.points = 10
        self.strength = 1
        self.frameindex = 0
        self.deathcount = 0

        #load images
        self.frames = [pygame.image.load(get_file_path("i","scobot" + "/scobot" + str(n) + ".png")) for n in range(4)]
        self.deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(10)]

        self.image.blit(self.frames[self.frameindex], (0,0))


    def draw(self,view):
        self.draw(view)

    def move(self,**kwargs):
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

        if self.frameindex > 2:
            self.frameindex = 0
        else:
            self.frameindex += 1
        if self.dead:
            self.rect.x = self.rect.x - self.vel
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.fill((255,255,255))
            if self.deathcount < 4:
                self.image.blit(self.frames[self.frameindex], (0,0))
            self.image.blit(self.deathSeq[self.deathcount],(-10,-10))
            if self.deathcount < 9:
                self.deathcount += 1
            else:
                #Set flag for removal
                self.remove = True
        else:
            self.rect.x = self.rect.x - self.vel
            self.image.blit(self.frames[self.frameindex], (0,0))

    def hit(self,hitval):
        self.strength -= hitval
        if self.strength <=0:
            self.dead = True


class BoagGunship(Collidable):
    def __init__(self, posx, posy, width, height):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 0
        self.shootcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable=True
        self.points = 10
        self.strength = 3
        self.frameindex = 0
        self.deathcount = 0

        #For targeting the player
        self.targety = None

        #load images
        self.frames = [pygame.image.load(get_file_path("i","boagship" + "/boag" + str(n) + ".png")) for n in range(4)]
        self.deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(18)]

        self.image.blit(self.frames[self.frameindex], (0,0))

    def draw(self,view):
        self.draw(view)

    def move(self,**kwargs):
        map = kwargs["map"]

        if self.frameindex < 3:
            self.frameindex += 1
        else:
            self.frameindex = 0
        if self.dead:
            self.rect.x = self.rect.x - self.vel
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.fill((255,255,255))
            if self.deathcount < 4:
                self.image.blit(self.frames[self.frameindex], (0,0))
            self.image.blit(self.deathSeq[self.deathcount],(-10,-10))
            if self.deathcount < 17:
                self.deathcount += 1
            else:
                #Set flag for removal
                self.remove = True
        else:
            if self.rect.y in range(kwargs["playery"]-5,kwargs["playery"]+5):
                #Shoot because the ship has crossed paths with the player
                if self.shootcounter == 0:
                    map.addprojectile(EnemyProjectileLeft(self.rect.x, self.rect.y + (self.height / 2), 20,10))
                #control rate of fire
                if self.shootcounter < 10:
                    self.shootcounter += 1
                else:
                    self.shootcounter = 0

            if not self.targety:
                #initialize  - targety is a point in time we don't want it to mirror the player
                self.targety = kwargs["playery"]

            #Home in on player
            if self.rect.y not in range(self.targety-5,self.targety+5):
                if self.rect.y > self.targety:
                    self.rect.y -= 2
                else:
                    self.rect.y += 2
            else:
                #Shoot
                if self.shootcounter == 0:
                    map.addprojectile(EnemyProjectileLeft(self.rect.x, self.rect.y + (self.height / 2), 20,10))
                #control rate of fire
                if self.shootcounter < 10:
                    self.shootcounter += 1
                else:
                    self.shootcounter = 0
                #Reset target now that ship has moved
                self.targety = kwargs["playery"]
                #Move to player
            self.image.blit(self.frames[self.frameindex], (0,0))
            self.rect.x -= self.vel

    def hit(self,hitval):
        self.strength -= hitval
        if self.strength <=0:
            self.dead = True

class EnemyGroup():
    def __init__(self, posx, posy, height):
        self.enemies = []
        self.x = posx
        self.y = posy
        self.startpos = posy
        self.endpos = posy + ( 30 * (height-1))


class ScobotGroup(EnemyGroup):
    def __init__(self, posx, posy, height):
        EnemyGroup.__init__(self,posx,posy,height)
        self.enemies.append(Scobot(self.x,self.y,20,30,False))
        self.movecount = 5

        for i in range(height-1):
            self.x = self.x + 25
            self.y = self.y + 30
            self.enemies.append(Scobot(self.x,self.y,20,30,False))
        #go backwards
        for i in range(height-1):
            self.x = self.x + 25
            self.y = self.y - 30
            self.enemies.append(Scobot(self.x,self.y,20,30,True))



    def draw(self,view):
        for s in self.enemies:
            s.draw(view)

    def move(self,**kwargs):
        #Move count controls the speed it animates at
        if self.movecount == 0:
            for s in self.enemies:
                if s.rect.y == self.startpos:
                    s.rect.y += 5
                    s.movingdown = True
                elif s.rect.y == self.endpos:
                    s.rect.y -= 5
                    s.movingdown = False
                else:
                    if s.movingdown:
                        s.rect.y += 5
                    else:
                        s.rect.y -= 5
            self.movecount = 5
        else:
            self.movecount -= 1
