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

        self.frames = [pygame.image.load(get_file_path("i","projbas" + "/projbas" + str(n) + ".png")) for n in range(9)]

        self.image.blit(self.frames[0], (0,0))

    def move(self):
        self.image.blit(self.frames[self.shootcount], (0,0))
        self.rect.x += self.vel
        if self.shootcount < 8:
            self.shootcount += 1

    """
    def hit(self):
        self.dead = True
        """
