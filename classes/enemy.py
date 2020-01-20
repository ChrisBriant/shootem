from include import get_file_path
from .collidables import Collidable
import pygame, os


class Rocket(Collidable):

    def __init__(self, posx, posy, width, height):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.launchcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

        #load images
        self.frames = [pygame.image.load(get_file_path("i","rocket" + "/rocket" + str(n) + ".png")) for n in range(5)]
                    #pygame.image.load(get_file_path("i",imagepath + "/EL1.png")),
                    #pygame.image.load(get_file_path("i",imagepath + "/EL2.png")),
                    #pygame.image.load(get_file_path("i",imagepath + "/EL3.png")),
                    #pygame.image.load(get_file_path("i",imagepath + "/EL4.png")),
                    #pygame.image.load(get_file_path("i",imagepath + "/EL5.png")),
                    #pygame.image.load(get_file_path("i",imagepath + "/EL6.png")),
                    #pygame.image.load(get_file_path("i",imagepath + "/EL7.png")),
                    #pygame.image.load(get_file_path("i",imagepath + "/EL8.png"))]

        self.image.blit(self.frames[0], (0,0))

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

    def draw(self,view):
        print("Drawing")
        self.draw(view)

    def move(self):
        print("moving")
        self.launchcounter += 1
        if self.launchcounter > 30:
            if self.launchcounter - 30 < 5:
                #animage the launch
                self.image.blit(self.frames[self.launchcounter-30], (0,0))
            self.rect.y -= self.vel

    #Animate the explosion
    def die(self):
        pass
