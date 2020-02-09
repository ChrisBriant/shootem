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
            self.gamearea = {"w":10000,"h":600}
            self.map.gamearea = self.gamearea
            #self.player.rect.x = 100
            #self.player.rect.y = 300
            self.player.rect.x = 9900
            self.player.rect.y = 300

            #Add objects
            self.map.addenemy(Scobot(600,100,20,30))
            self.map.addenemy(Scobot(650,200,20,30))
            self.map.addenemy(Scobot(700,250,20,30))
            self.map.addenemy(Scobot(1000,200,20,30))
            self.map.addenemy(Scobot(1050,250,20,30))
            self.map.addenemy(Scobot(1100,350,20,30))
            self.map.addenemygroup(ScobotGroup(1400,300,5))
            self.map.addenemygroup(ScobotGroup(2000,100,5))
            self.map.addcollidable(Wall(1800,250,8))
            self.map.addenemy(Scobot(2250,500,20,30))
            self.map.addenemy(Scobot(2550,300,20,30))
            self.map.addenemy(Scobot(2550,400,20,30))
            self.map.addenemy(BoagPulse(2900,200,30,30,True,True))
            self.map.addenemy(BoagPulse(3200,300,30,30,True,True))
            self.map.addenemy(BoagPulse(3400,100,30,30,True,True))
            self.map.addenemygroup(ScobotGroup(3500,400,5))
            self.map.addenemygroup(ScobotGroup(3800,200,5))
            self.map.addcollidable(Wall(4100,200,8))
            self.map.addenemy(BoagPulse(4600,50,30,30,True,True))
            self.map.addenemy(BoagPulse(4600,450,30,30,True,True))
            self.map.addenemygroup(BoagPulseGroup(5200,50,2,False))
            self.map.addenemygroup(BoagPulseGroup(5000,250,2,False))
            self.map.addenemygroup(BoagPulseGroup(5400,400,2,False))
            self.map.addenemy(Kamakazie(5700,100,55,20))
            self.map.addenemy(Kamakazie(5800,100,55,20))
            self.map.addenemy(Scobot(5600,50,20,30))
            self.map.addenemy(Scobot(5700,500,20,30))
            self.map.addenemy(BoagPulse(6000,150,30,30,True,True))
            self.map.addcollidable(Wall(6100,0,15))
            self.map.addcollidable(Wall(6500,200,15))
            self.map.addcollidable(Wall(7000,0,15))
            self.map.addenemy(Scobot(6300,500,20,30))
            self.map.addenemy(Scobot(6700,100,20,30))
            self.map.addenemy(Scobot(7300,500,20,30))
            self.map.addenemygroup(ScobotWall(7500,100,15))
            self.map.addenemygroup(ScobotWall(7800,200,10))
            self.map.addenemygroup(ScobotWall(8000,100,15))
            self.map.addcollidable(Wall(8200,0,6))
            self.map.addcollidable(Wall(9380,0,6))
            self.map.addcollidable(Floor1(8200,170,40))
            self.map.addcollidable(Floor1(8200,400,40))
            self.map.addcollidable(Wall(8200,430,6))
            self.map.addcollidable(Wall(9380,430,6))
            self.map.addenemy(GunUpDown(8400,200,20,30))
            self.map.addenemy(GunUpDown(8600,370,20,30,False))
            self.map.addenemygroup(ScobotGroup(9000,250,5))
            self.map.addenemygroup(ScobotGroup(9300,250,5))
            self.map.addenemy(GunUpDown(8800,200,20,30))
            self.map.addenemy(GunUpDown(9000,370,20,30,False))
            self.map.addcollidable(Wall(9980,0,20))
            self.map.addenemy(BoagGunship(9800,200,60,40))
            #self.map.addcollidable(Wall(600,0,10))
            #self.map.addcollidable(Wall(1200,100,10))
            #self.map.addcollidable(Wall(2300,100,10))
