from include import get_file_path
from .collidables import Collidable
import pygame, os

class GameMap(pygame.sprite.Sprite):

    def __init__(self, gamearea, screen):
        self.gamearea = gamearea
        self.screen = screen
        self.collidables = pygame.sprite.Group()

    def addcollidable(self, posx, posy, width, height):
        self.collidables.add(Collidable(posx,posy,width,height))

    def addenemy(self, sprite):
        self.collidables.add(sprite)

    #Gets the collidable objects to draw on screen
    def getcollidables(self,xoffset):
        onscreensprites = pygame.sprite.Group()

        for collidable in self.collidables.sprites():
            #print(str(id(collidable)))
            if collidable.onscreen(xoffset*-1,self.screen):
                if(collidable.movable):
                    collidable.move()
                onscreensprites.add(collidable)
        return onscreensprites

    def collision(self,sprite):
        sprite = pygame.sprite.spritecollideany(sprite,self.collidables)
        if sprite:
            return True
        else:
            return False
