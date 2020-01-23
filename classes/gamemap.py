from include import get_file_path
from .collidables import Collidable
import pygame, os

class GameMap(pygame.sprite.Sprite):

    def __init__(self, gamearea, screen, player):
        self.gamearea = gamearea
        self.screen = screen
        self.collidables = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.player = player

    def addcollidable(self, posx, posy, width, height):
        self.collidables.add(Collidable(posx,posy,width,height))

    def addenemy(self, sprite):
        self.collidables.add(sprite)

    def addprojectile(self,sprite):
        self.projectiles.add(sprite)

    #Gets the collidable objects to draw on screen
    def getcollidables(self,xoffset):
        onscreensprites = pygame.sprite.Group()
        collidables = self.collidables.sprites() + self.projectiles.sprites()

        for collidable in self.collidables.sprites():
            #print(str(id(collidable)))
            if collidable.onscreen(xoffset*-1,self.screen):
                if(collidable.movable):
                    collidable.move()
                onscreensprites.add(collidable)
        return onscreensprites

    def collision(self):
        sprite = pygame.sprite.spritecollideany(self.player,self.collidables)
        if sprite:
            return True
        else:
            return False
