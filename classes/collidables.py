from include import get_file_path, collideontop
import pygame, os

class Collidable(pygame.sprite.Sprite):

    def __init__(self, posx, posy, width, height,movable=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.projectile = False

        self.image.fill((0,255,0))

        self.movable = movable
        self.destructable = False
        self.points = 0
        self.strength = 0

        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.width = width
        self.height = height
        self.dead = False
        self.remove = False

    def onscreen(self,xoffset,screen):
        #Caculate object within screen area
        screenend = screen["w"] + xoffset
        if self.rect.x  + self.rect.width > xoffset and self.rect.x < screenend:
            return True
        else:
            return False

    #Method not used at the moment
    def isdeleteable(xoffset):
        if self.rect.x - 10 > xoffset:
            return True
        else:
            return False

    def hit(self,hitval,**kwargs):
        map = kwargs["map"]

        self.strength -= hitval
        #Not self.dead prevents scoring more than once
        if self.strength <=0 and not self.dead:
            self.dead = True
            map.scoreboard.addscore(self.points)

class Wall(Collidable):

    ## NOTE: Height is in blocks
    def __init__(self,posx,posy,height):
        Collidable.__init__(self,posx,posy,20,(30*height))
        self.vel = 3
        self.launchcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable = False
        #There is a minimum height of three
        if height < 3:
            height = 3
        self.topend = pygame.image.load(get_file_path("i","wall1/wall11.png"))
        self.botend = pygame.image.load(get_file_path("i","wall1/wall12.png"))
        self.midsec = pygame.image.load(get_file_path("i","wall1/wall10.png"))
        #Draw the wall
        for i in range(0,height):
            print(i)
            if i == 0:
                self.image.blit(self.topend, (0,0))
            elif i == height:
                print("HELLO MAN")
                self.image.blit(self.botend, (0,i*30))
            else:
                self.image.blit(self.midsec, (0,i*30))
