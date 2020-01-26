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
        self.enemygroups = []

    def addcollidable(self, posx, posy, width, height):
        self.collidables.add(Collidable(posx,posy,width,height))

    def addenemy(self, sprite):
        self.collidables.add(sprite)

    def addenemygroup(self, enemygroup):
        self.enemygroups.append(enemygroup)

        for e in enemygroup.enemies:
            print(e)
            self.collidables.add(e)

    def addprojectile(self,sprite):
        self.projectiles.add(sprite)

    #Gets the collidable objects to draw on screen
    def getcollidables(self,xoffset):
        onscreensprites = pygame.sprite.Group()
        projectiles = self.projectiles.sprites()
        #Remove unwanted projectiles
        for p in projectiles:
            if not p.onscreen(xoffset*-1,self.screen):
                self.projectiles.remove(p)
                del p
        collidables = self.collidables.sprites() + projectiles

        print("Col count", ",", len(projectiles))

        for collidable in collidables:
            #Remove if it has been destroyed
            if collidable.remove:
                self.collidables.remove(collidable)
            #Animate
            if collidable.onscreen(xoffset*-1,self.screen):
                if(collidable.movable):
                    collidable.move(playery=self.player.rect.y,map=self)
                onscreensprites.add(collidable)

        #Update movement for enemy groups
        [eg.move() for eg in self.enemygroups]
        return onscreensprites

    #Detect a projectile hitting an enemy and perform action
    def updatecollidables(self,onscreensprites):
        sprites = []
        friendlyprojectiles = [p for p in self.projectiles if not p.enemy]
        for proj in friendlyprojectiles:
            collided = pygame.sprite.spritecollide(proj,onscreensprites, False)
            hitval = sum([ s.hitval for s in collided if type(s).__name__=="Projectile"])
            for sprite in collided:
                if sprite.destructable:
                    sprite.hit(hitval)
                    self.projectiles.remove(proj)

                sprites.append(sprite)

    def collision(self):
        sprite = pygame.sprite.spritecollideany(self.player,self.collidables)
        if sprite:
            return True
        else:
            return False
