from include import get_file_path
from .collidables import Collidable
import pygame, os

class Projectile(Collidable):

    def __init__(self, posx, posy, width, height):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

    def move(self):
        self.image.blit(self.image, (0,0))
        self.rect.y -= self.vel
