from include import get_file_path
from .enemy import *
from .collidables import *
from .gamemap import GameMap
import pygame, os


class Level():

    def __init__(self, player, screen):
        self.gamearea = {"w":0,"h":0 }
        self.player = player
        self.map = GameMap(self.gamearea,screen,player)


    def loadlevel(self,levelnumber):
        if levelnumber == 1:
            #Define level 1
            self.gamearea = {"w":3000,"h":600}
            self.map.gamearea = self.gamearea
            self.player.rect.x = 100
            self.player.rect.y = 300

            #Add objects
            self.map.addcollidable(Wall(600,0,10))
            self.map.addcollidable(Wall(1200,100,10))
            self.map.addcollidable(Wall(2300,100,10))
