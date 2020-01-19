from include import get_file_path
from .collidables import Collidable
import pygame, os


class Rocket(Collidable):

    def __init__(self, posx, posy, width, height):
        Collidable.__init__(self,posx,posy,width,height)
        self.vel = 3

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

    def move(self):
        self.rect.y += self.vel
