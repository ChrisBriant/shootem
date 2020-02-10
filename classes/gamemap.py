from include import get_file_path
from .collidables import Collidable
from .scoreboard import ScoreBoard
import pygame, os

#Static method to get the enemies which collide with each other
def enemiescollidewitheachother(enemyspritegroup):
    enemiescollided = []
    for e in enemyspritegroup:
        collisions = pygame.sprite.spritecollide(e,enemyspritegroup,False)
        enemiescollided.append([collided for collided in collisions if collided != e])
    return [i for list in enemiescollided for i in list]

class GameMap(pygame.sprite.Sprite):

    def __init__(self, gamearea, screen, player):
        self.gamearea = gamearea
        self.screen = screen
        self.collidables = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.collectables = pygame.sprite.Group()
        #self.enemies = pygame.sprite.Group()
        self.player = player
        self.enemygroups = []
        self.scoreboard = ScoreBoard(screen, player.lives)
        self.enemieskilled = 0

    def addcollidable(self, collidable):
        self.collidables.add(collidable)

    def addenemy(self, sprite):
        #Add to collidable group as well as enemy group for easier sorting
        #self.enemies.add(sprite)
        self.collidables.add(sprite)

    def addenemygroup(self, enemygroup):
        self.enemygroups.append(enemygroup)

        for e in enemygroup.enemies:
            print(e)
            self.collidables.add(e)

    def getenemygroup(self,sprite):
        enemygroup = None

        for eg in self.enemygroups:
            for e in eg.enemies:
                if sprite == e:
                    enemygroup = eg
        return enemygroup


    def addprojectile(self,sprite):
        self.projectiles.add(sprite)

    def addcollectable(self, collectable):
        self.collectables.add(collectable)

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

        for collidable in collidables:
            #Remove if it has been destroyed
            if collidable.remove:
                self.collidables.remove(collidable)

            #Animate
            #Moving whole group
            if collidable.group:
                group = self.getenemygroup(collidable)
                if group.onscreen(xoffset*-1,self.screen):
                    if collidable.movable:
                        collidable.move(playerx=self.player.rect.x,playery=self.player.rect.y,map=self,xoffset=xoffset*-1)
                    onscreensprites.add(collidable)
            #Only display if onscreen and not group
            if collidable.onscreen(xoffset*-1,self.screen) and not collidable.group:
                if(collidable.movable):
                    collidable.move(playerx=self.player.rect.x,playery=self.player.rect.y,map=self,xoffset=xoffset*-1)
                onscreensprites.add(collidable)
        #Animate collectables
        onscreencollectables = [c for c in self.collectables if c.onscreen(xoffset*-1,self.screen)]
        [c.move() for c in onscreencollectables]
        [onscreensprites.add(c) for c in onscreencollectables]
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
                    sprite.hit(hitval,map=self)
                    self.projectiles.remove(proj)
                sprites.append(sprite)
        #Detect enemies hitting each other
        #Filter the onscreen sprites into two groups
        enemyspritesonscreen = pygame.sprite.Group()
        furnitureonscreen = pygame.sprite.Group()
        projectilesonscreen = pygame.sprite.Group()

        for sprite in onscreensprites:
            if sprite.destructable:
                enemyspritesonscreen.add(sprite)
            elif sprite.projectile:
                projectilesonscreen.add(sprite)
            else:
                furnitureonscreen.add(sprite)
        collidedsprites = pygame.sprite.groupcollide(enemyspritesonscreen,furnitureonscreen,False,False)
        #print(collidedsprites)
        for sprite in collidedsprites:
            if sprite.destructable:
                sprite.dead = True
        #Deals with projectiles colliding with furniture it needs to be removed
        collidedprojectiles = pygame.sprite.groupcollide(projectilesonscreen,furnitureonscreen,False,False)
        for sprite in collidedprojectiles:
            if sprite.projectile:
                self.projectiles.remove(sprite)
        #Deal with enemies colliding with each other
        for e in enemiescollidewitheachother(enemyspritesonscreen):
            e.dead = True
        #Deal with collectables
        collidedcollectables = pygame.sprite.spritecollide(self.player,self.collectables,False)
        [c.performaction() for c in collidedcollectables]


    def collision(self):
        enemyprojectiles = [p for p in self.projectiles if p.enemy]
        collidables = [c for c in self.collidables]
        enemycollidables = collidables + enemyprojectiles
        sprite = pygame.sprite.spritecollideany(self.player,enemycollidables)
        if sprite:
            return True
        else:
            return False
