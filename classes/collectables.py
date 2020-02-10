from include import get_file_path
from .collidables import Collidable
from .screenmessage import OnScreenMessage,FlashingText
import pygame, os

class Collectable(Collidable):

    def __init__(self,posx,posy,width,height):
        Collidable.__init__(self, posx, posy, width, height)
        self.destructable = False

    #Performs the action that the collictivle object has
    def performaction(self,**kwargs):
        pass

#Takes the player to a new level
class WormHole(Collectable):
    def __init__(self,posx,posy,width,height,level):
        Collectable.__init__(self, posx, posy, width, height)
        self.frames = [pygame.image.load(get_file_path("i","wormhole" + "/w-hole" + str(n) + ".png")) for n in range(15)]
        self.frameindex = 0
        self.level=level

    def performaction(self):
        #change level
        #player = kwargs["player"]
        #map = kwargs["map"]
        #level = kwargs["level"]
        self.level.levelovermessage = OnScreenMessage(70,"Level " + str(self.level.levelno) + " complete")
        self.level.loadlevel(self.level.levelno+1)
        self.level.leveltrans = True

    def move(self,**kwargs):
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.image.blit(self.frames[self.frameindex], (0,0))
        self.frameindex += 1
        if self.frameindex > 14:
            self.frameindex = 10