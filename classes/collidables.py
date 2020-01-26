from include import get_file_path, collideontop
import pygame, os

class Collidable(pygame.sprite.Sprite):

    def __init__(self, posx, posy, width, height,movable=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))

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

    def hit(self):
        print("Hit")
