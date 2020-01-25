from include import get_file_path
from .collidables import Collidable
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

    def move(self):
        self.launchcounter += 1
        if self.launchcounter > 30:
            if self.launchcounter - 30 < 5:
                #animage the launch
                self.image.blit(self.frames[self.launchcounter-30], (0,0))
            self.rect.y -= self.vel

    #Animate the explosion
    def hit(self):
        pass


class Scobot(Collidable):
    def __init__(self, posx, posy, width, height, movingdown):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.launchcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.movingdown=movingdown
        self.destructable=True
        self.points = 10
        self.strength = 1

        #load images
        self.frames = [pygame.image.load(get_file_path("i","scobot" + "/scobot" + str(n) + ".png")) for n in range(4)]

        self.image.blit(self.frames[0], (0,0))


    def draw(self,view):
        self.draw(view)

    def move(self):
        self.rect.x = self.rect.x - self.vel

    def hit(self,hitval):
        if self.strength - hitval <=0:
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

    def move(self):
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
