from include import get_file_path
from .collidables import Collidable
import pygame, os

class Projectile(Collidable):

    def __init__(self, posx, posy, width, height):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 10
        self.shootcount = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable = False
        self.hitval = 1
        self.enemy = False #Means projectile from the player
        self.projectile = True

        self.frames = [pygame.image.load(get_file_path("i","projbas" + "/projbas" + str(n) + ".png")) for n in range(9)]

        self.image.blit(self.frames[0], (0,0))

    def move(self,**kwargs):
        self.image.blit(self.frames[self.shootcount], (0,0))
        self.rect.x += self.vel
        if self.shootcount < 8:
            self.shootcount += 1

    """
    def hit(self):
        self.dead = True
        """

#Shoots a projectile to the left of the screen
class EnemyProjectileLeft(Projectile):

    def __init__(self,posx,posy,width,height):
        Projectile.__init__(self,posx,posy,width,height)
        self.enemy = True
        self.frames = [pygame.image.load(get_file_path("i","projboag" + "/projboag" + str(n) + ".png")) for n in range(14)]

        self.image.blit(self.frames[0], (0,0))

    def move(self,**kwargs):
        self.image.blit(self.frames[self.shootcount], (0,0))
        self.rect.x -= self.vel
        if self.shootcount < 13:
            self.shootcount += 1


#Shoots a projectile to the left of the screen
class EnemyProjectileDown(Projectile):

    def __init__(self,posx,posy,width,height):
        Projectile.__init__(self,posx,posy,width,height)
        self.enemy = True
        self.frames = [pygame.image.load(get_file_path("i","projd" + "/projd" + str(n) + ".png")) for n in range(17)]

        self.image.blit(self.frames[0], (0,0))

    def move(self,**kwargs):
        self.image.blit(self.frames[self.shootcount], (0,0))
        self.rect.y += self.vel
        if self.shootcount < 16:
            self.shootcount += 1


#Shoots a projectile to the left of the screen
class EnemyProjectileUp(Projectile):

    def __init__(self,posx,posy,width,height):
        Projectile.__init__(self,posx,posy,width,height)
        self.enemy = True
        self.frames = [pygame.image.load(get_file_path("i","projd" + "/projd" + str(n) + ".png")) for n in range(17)]

    def move(self,**kwargs):
        self.image.blit(pygame.transform.flip(self.frames[self.shootcount],False,True), (0,0))
        self.rect.y -= self.vel
        if self.shootcount < 16:
            self.shootcount += 1


#Shoot a projectile diagonaly
class EnemyProjectileDiagonal(Projectile):

    def __init__(self,posx,posy,width,height,angle,right=False):
        Projectile.__init__(self,posx,posy,width,height)
        self.enemy = True
        self.right = right
        self.frames = [pygame.image.load(get_file_path("i","projboag" + "/projboag" + str(n) + ".png")) for n in range(14)]
        self.angle = angle

    def move(self,**kwargs):
        if self.right:
            self.image.fill((255,255,255))
            self.image.set_colorkey((255,255,255))
            self.image.blit(pygame.transform.rotate(self.frames[self.shootcount],(180 - self.angle)*-1), (0,0))
            self.rect.y -= self.vel
            self.rect.x += self.vel
        else:
            self.image.fill((255,255,255))
            self.image.set_colorkey((255,255,255))
            self.image.blit(pygame.transform.rotate(self.frames[self.shootcount],self.angle*-1), (0,0))
            self.rect.y -= self.vel
            self.rect.x -= self.vel
        if self.shootcount < 13:
            self.shootcount += 1
