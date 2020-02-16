from include import get_file_path, collideontop
from .projectiles import Projectile
import pygame, os

class Player(pygame.sprite.Sprite):
    moveForward = [pygame.image.load(get_file_path("i","shipf" + "/shipf" + str(n) + ".png")) for n in range(9)]
    moveBack = [pygame.image.load(get_file_path("i","shipr" + "/shipr" + str(n) + ".png")) for n in range(9)]

    deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(20)]
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, x, y, width, height, lives=3):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface((width, height))
       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.width = width
       self.height = height
       self.vel = 5
       self.isJump = False
       self.left = False
       self.right = False
       self.up = False
       self.down = False
       self.walkCount = 0
       self.jumpCount = 0
       self.standing = True
       self.grounded = False
       self.dead = False
       self.lives = lives
       self.deathCount = 0
       self.death_drop_count = 5
       self.deathpos = (0,0)
       self.rateoffirecount = 0
       #Initiation
       self.init = True
       self.initcount = 0
       self.alpha = 255
       self.newlevel = False


    def hit(self):
        print("Hit Goblin!")

    def draw(self, view):
        #self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.image.set_alpha(self.alpha) #Set transparancy

        if self.walkCount + 1 > 9:
            self.walkCount = 7
        if self.standing:
            self.walkCount = 0

        #Control transparancy on initiation of player for invulnerability at start of level
        if self.init and self.initcount % 10 != 0:
            self.alpha -= 25.5
        else:
            self.alpha = 255

        if self.initcount >= 100:
            #Blank out for testing -make permanently invulnerable
            self.init = False
            self.alpha = 255
        else:
            self.initcount += 1

        if self.dead:
            #Animate death sequence
            #increase image size first
            self.image = pygame.transform.scale(self.image,(50,50))
            #self.image.fill((255,255,255))
            #self.image.set_colorkey((255,255,255))
            self.image.blit(self.moveForward[0], (0,0))
            self.image.blit(self.deathSeq[self.deathCount], (0,0))
            if self.deathCount < 19:
                #print(self.deathCount)
                self.deathCount += 1
        else:
            #Normal movement
            if not(self.standing):
                if self.left:
                    self.image.blit(self.moveBack[self.walkCount], (0,0))
                    self.walkCount += 1
                elif self.right:
                    self.image.blit(self.moveForward[self.walkCount], (0,0))
                    self.walkCount +=1
            else:
                if self.right:
                    self.image.blit(self.moveForward[0], (0,0))
                else:
                    self.image.blit(self.moveBack[0], (0,0))
        view.blit(self.image,(self.rect.x,self.rect.y))

    def moveleft(self):
        self.rect.x -= self.vel
        self.left = True
        self.right = False
        self.up = False
        self.down = False
        self.standing = False

    def moveright(self):
        self.rect.x += self.vel*2
        self.right = True
        self.left = False
        self.up = False
        self.down = False
        self.standing = False

    def moveup(self):
        self.rect.y -= self.vel
        self.right = True
        self.left = False
        self.up = False
        self.down = False
        self.standing = False

    def movedown(self):
        self.rect.y += self.vel
        self.right = True
        self.left = False
        self.up = False
        self.down = False
        self.standing = False


    def moveplayer(self,keys,screen, gamearea,map,xoffset):
        #Update the map with the player position
        #map.playerpos = (self.rect.x,self.rect.y)

        if self.dead:
            #Move player up and then off the screen
            if self.death_drop_count > 0:
                if self.rect.y > 0:
                    self.rect.y -= 6
                    self.death_drop_count -= 1
            else:
                self.rect.y += 6
        else:
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.moveleft()
            elif keys[pygame.K_RIGHT] and self.rect.x < gamearea["w"] - self.width and not self.rect.x > xoffset + (screen["w"] - (self.width + 10)):
                self.moveright()
            #Need to stop player hitting bottom of scoreboard
            elif keys[pygame.K_UP] and self.rect.y > map.scoreboard.height:
                self.moveup()
            elif keys[pygame.K_DOWN] and self.rect.y < gamearea["h"] - self.height:
                self.movedown()
            elif keys[pygame.K_SPACE]:
                if self.rateoffirecount <= 0:
                    map.addprojectile(Projectile(self.rect.x + self.width, self.rect.y + (self.height / 2), 20,5))
                    self.rateoffirecount = 4
                    #print(map.gamearea)
                else:
                    #Control rate of fire
                    self.rateoffirecount -= 1
            else:
                self.standing = True
                self.rect.x += 1
                self.walkCount = 0

            #Set jump in motion
            """
            if keys[pygame.K_UP] and self.jumpCount <= 0 and self.grounded:
                self.jumpCount = 10
                self.grounded = False #in the air

            if self.jumpCount > 0 and self.jumpCount <= 10:
                print("Jump",self.rect.y)
                if self.rect.y > 0:
                    self.rect.y -= 12
                    self.jumpCount -= 1
                else:
                    self.jumCount = 0
                    """
    #Get location to scroll the screen along x axis when the man moves
    def calculatexoffset(self,screen,gamearea):
        if self.rect.x - screen["w"]//2 >= 0 and self.rect.x < gamearea["w"] - screen["w"]//2:
            xoffset =  screen["w"]//2 - self.rect.x
        elif self.rect.x - screen["w"]//2 < 0:
            xoffset = 0
        else:
            xoffset = screen["w"] - gamearea["w"]
        return xoffset

    #Get location to scroll the screen along y axis when the man moves
    def calculateyoffset(self,screen,gamearea):
        if self.rect.y > screen["h"] // 2 and gamearea["h"] - self.rect.y > (screen["h"] // 2) - 10:
            yoffset = 5 + (screen["h"] // 2) - self.rect.y
        elif gamearea["h"] - self.rect.y < (screen["h"] // 2):
            yoffset = (screen["h"]) - gamearea["h"]
        else:
            yoffset = 0
        return yoffset

    #Detect screen catching player
    def catchscreen(self, xoffset):
        xoffset = xoffset*-1
        #print(xoffset, ",",self.rect.x)
        if self.rect.x < xoffset:
            return True
        else:
            return False

    #Routine for player death
    def die(self,map,xoffset):
        if not self.dead and not self.init:
            self.dead = True
            self.lives -= 1
            map.scoreboard.updatelives(self.lives)
            #If statement below is for getting the player to jump forward if catching the screen
            #To stop the insta death after pressing space
            if self.rect.x < xoffset*-1:
                self.rect.x += 10 + self.width
            self.deathpos = (self.rect.x,self.rect.y)
