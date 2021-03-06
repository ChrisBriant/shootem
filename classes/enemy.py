from include import get_file_path
from .collidables import Collidable
from .projectiles import EnemyProjectileLeft, EnemyProjectileDown, EnemyProjectileUp, \
    EnemyProjectileDiagonal
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from random import randrange
import pygame, os, math



class Rocket(Collidable):

    def __init__(self, posx, posy, width, height):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.launchcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable = True

        #load images
        self.frames = [pygame.image.load(get_file_path("i","rocket" + "/rocket" + str(n) + ".png")) for n in range(5)]

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

    """
    def draw(self,view):
        print("Drawing")
        self.draw(view)
        """

    def move(self,**kwargs):
        self.launchcounter += 1
        if self.launchcounter > 30:
            if self.launchcounter - 30 < 5:
                #animage the launch
                self.image.blit(self.frames[self.launchcounter-30], (0,0))
            self.rect.y -= self.vel



class GunUpDown(Collidable):

    def __init__(self, posx, posy, width, height, down=True):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.shootcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable = False
        self.down = down

        #load images
        self.frame = pygame.image.load(get_file_path("i","gund0.png"))

        if down:
            self.image.blit(self.frame, (0,0))
        else:
            self.image.blit(pygame.transform.flip(self.frame, False, True), (0,0))


    def move(self,**kwargs):
        map = kwargs["map"]

        if self.down:
            if self.shootcounter == 0:
                map.addprojectile(EnemyProjectileDown(self.rect.x - 5, self.rect.y + self.height, 30,28))
            #control rate of fire
            if self.shootcounter < 30:
                self.shootcounter += 1
            else:
                self.shootcounter = 0
        else:
            if self.shootcounter == 0:
                map.addprojectile(EnemyProjectileUp(self.rect.x - 5, self.rect.y - self.height, 30,28))
            #control rate of fire
            if self.shootcounter < 30:
                self.shootcounter += 1
            else:
                self.shootcounter = 0




class Scobot(Collidable):
    def __init__(self, posx, posy, width, height, movingdown=True, group=False):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.movingdown=movingdown
        self.destructable=True
        self.points = 10
        self.strength = 1
        self.frameindex = 0
        self.deathcount = 0
        self.group = group

        #load images
        self.frames = [pygame.image.load(get_file_path("i","scobot" + "/scobot" + str(n) + ".png")) for n in range(4)]
        self.deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(10)]

        self.image.blit(self.frames[self.frameindex], (0,0))


    def draw(self,view):
        self.draw(view)

    def move(self,**kwargs):
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

        if self.frameindex > 2:
            self.frameindex = 0
        else:
            self.frameindex += 1
        if self.dead:
            self.rect.x = self.rect.x - self.vel
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.fill((255,255,255))
            if self.deathcount < 4:
                self.image.blit(self.frames[self.frameindex], (0,0))
            self.image.blit(self.deathSeq[self.deathcount],(-10,-10))
            if self.deathcount < 9:
                self.deathcount += 1
            else:
                #Set flag for removal
                self.remove = True
        else:
            self.rect.x = self.rect.x - self.vel
            self.image.blit(self.frames[self.frameindex], (0,0))


class BoagFighter(Collidable):
    def __init__(self, posx, posy, width, height, map):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable=True
        self.points = 30
        self.strength = 1
        self.frameindex = 0
        self.deathcount = 0
        #Control missile
        self.missilexoffset = 10
        self.missileyoffset = height + 5
        self.launched = False

        #Add the homing missile
        map.addenemy(HomingMissile(posx+self.missilexoffset,posy+self.missileyoffset,40,10,self))

        #load images
        self.frames = [pygame.image.load(get_file_path("i","boagfighter" + "/boagfight" + str(n) + ".png")) for n in range(9)]
        self.deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(18)]


    def move(self,**kwargs):
        playery = kwargs["playery"]

        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

        if self.frameindex >= 8:
            self.frameindex = 0
        else:
            self.frameindex += 1
        if self.dead:
            self.rect.x = self.rect.x - self.vel
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.fill((255,255,255))
            if self.deathcount < 4:
                self.image.blit(self.frames[self.frameindex], (0,0))
            self.image.blit(self.deathSeq[self.deathcount],(0,0))
            if self.deathcount < 17:
                self.deathcount += 1
            else:
                #Set flag for removal
                self.remove = True
        else:
            #Get position
            if self.rect.y not in range(playery-5,playery+5):
                if self.rect.y > playery:
                    self.rect.y -= 1
                else:
                    self.rect.y += 1
            else:
                #Launch missile
                self.launched = True
            self.rect.x = self.rect.x - self.vel
            self.image.blit(self.frames[self.frameindex], (0,0))


class BoagGunship(Collidable):
    def __init__(self, posx, posy, width, height):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 0
        self.shootcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable=True
        self.points = 40
        self.strength = 3
        self.frameindex = 0
        self.deathcount = 0

        #For targeting the player
        self.targety = None

        #load images
        self.frames = [pygame.image.load(get_file_path("i","boagship" + "/boag" + str(n) + ".png")) for n in range(4)]
        self.deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(18)]

        self.image.blit(self.frames[self.frameindex], (0,0))

    def draw(self,view):
        self.draw(view)

    def move(self,**kwargs):
        map = kwargs["map"]

        if self.frameindex < 3:
            self.frameindex += 1
        else:
            self.frameindex = 0
        if self.dead:
            self.rect.x = self.rect.x - self.vel
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.fill((255,255,255))
            if self.deathcount < 4:
                self.image.blit(self.frames[self.frameindex], (0,0))
            self.image.blit(self.deathSeq[self.deathcount],(-10,-10))
            if self.deathcount < 17:
                self.deathcount += 1
            else:
                #Set flag for removal
                self.remove = True
        else:
            if self.rect.y in range(kwargs["playery"]-5,kwargs["playery"]+5):
                #Shoot because the ship has crossed paths with the player
                if self.shootcounter == 0:
                    map.addprojectile(EnemyProjectileLeft(self.rect.x-20, self.rect.y + (self.height / 2), 20,10))
                #control rate of fire
                if self.shootcounter < 10:
                    self.shootcounter += 1
                else:
                    self.shootcounter = 0

            if not self.targety:
                #initialize  - targety is a point in time we don't want it to mirror the player
                self.targety = kwargs["playery"]

            #Home in on player
            if self.rect.y not in range(self.targety-5,self.targety+5):
                if self.rect.y > self.targety:
                    self.rect.y -= 2
                else:
                    self.rect.y += 2
            else:
                #Shoot
                if self.shootcounter == 0:
                    map.addprojectile(EnemyProjectileLeft(self.rect.x-20, self.rect.y + (self.height / 2), 20,10))
                #control rate of fire
                if self.shootcounter < 10:
                    self.shootcounter += 1
                else:
                    self.shootcounter = 0
                #Reset target now that ship has moved
                self.targety = kwargs["playery"]
                #Move to player
            self.image.blit(self.frames[self.frameindex], (0,0))
            self.rect.x -= self.vel

    """
    def hit(self,hitval):
        self.strength -= hitval
        if self.strength <=0:
            self.dead = True
            """
class TargetTriangle():
    def __init__(self, posx, posy, angle1, angle2, length):
        self.length = length
        self.angle1 = angle1
        self.angle2 = angle2
        self.point0 = (posx,posy)
        self.point1 = (self.point0[0] - math.cos(math.radians(angle1)) * length, self.point0[1] - math.sin(math.radians(angle1)) * length)
        self.point2 = (self.point0[0] - math.cos(math.radians(angle2)) * length, self.point0[1] - math.sin(math.radians(angle2)) * length)

        # then render the line radar->(x,y)
        #pygame.draw.line(screen, Color("red"), line, (x,y), 1)

    def updateposition(self,posx,posy,reverse=False):
        if reverse:
            angle1 = 180 - self.angle1
            angle2 = 180 - self.angle2
        else:
            angle1 = self.angle1
            angle2 = self.angle2
        self.point0 = (posx,posy)
        self.point1 = (self.point0[0] - math.cos(math.radians(angle1)) * self.length, self.point0[1] - math.sin(math.radians(angle1)) * self.length)
        self.point2 = (self.point0[0] - math.cos(math.radians(angle2)) * self.length, self.point0[1] - math.sin(math.radians(angle2)) * self.length)

    def getpoints(self):
        return (self.point0,self.point1,self.point2)

    #Detects the presence of a sprite inside the targeting triangle
    def spriteinside(self,spritex,spritey):
        point = Point(spritex, spritey)
        points = self.getpoints()
        polygon = Polygon([points[0], points[1], points[2]])
        return polygon.contains(point)

class BoagSpider(Collidable):
    def __init__(self, posx, posy, width, height, leftlimit, rightlimit):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.width = width
        self.height = height
        self.shootcounter = 20
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable=True
        self.points = 40
        self.strength = 2
        self.frameindex = 0
        self.deathcount = 0
        self.leftlimit = leftlimit
        self.rightlimit = rightlimit
        self.movingleft = True
        self.frameindex = 0
        self.animatecount = 0
        self.targetingtriangle = TargetTriangle(self.rect.x,self.rect.y,35,70,400)

        #For targeting the player
        self.targety = None


        #load images
        self.frames = [pygame.image.load(get_file_path("i","boagspider" + "/spider" + str(n) + ".png")) for n in range(9)]
        self.framesright = [pygame.image.load(get_file_path("i","boagspider-rght" + "/spider-r" + str(n) + ".png")) for n in range(9)]
        self.deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(18)]


    def move(self,**kwargs):
        map = kwargs["map"]
        xoffset = kwargs["xoffset"]
        playerx = kwargs["playerx"]
        playery = kwargs["playery"]

        if self.animatecount < 4:
            self.animatecount += 1
        else:
            self.animatecount = 0
            if self.frameindex < 8:
                self.frameindex += 1
            else:
                self.frameindex = 0
        if self.dead:
            self.rect.x = self.rect.x - self.vel
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.fill((255,255,255))
            if self.deathcount < 4:
                self.image.blit(self.frames[self.frameindex], (0,0))
            self.image.blit(self.deathSeq[self.deathcount],(0,0))
            if self.deathcount < 17:
                self.deathcount += 1
            else:
                #Set flag for removal
                self.remove = True
        else:
            #print(self.rect.x,self.pathlimit, self.movingleft, xoffset+map.screen["w"])
            if self.rect.x <= self.leftlimit:
                self.movingleft = False
            elif self.rect.x >= self.rightlimit:
                self.movingleft = True

            self.image.fill((255,255,255))
            if self.movingleft:
                self.rect.x -= self.vel
                #Update targeting triangle
                self.targetingtriangle.updateposition(self.rect.x,self.rect.y)
                self.image.blit(self.frames[self.frameindex], (0,0))
            else:
                self.rect.x += self.vel
                #Update targeting triangle
                self.targetingtriangle.updateposition(self.rect.x+self.width,self.rect.y,True)
                self.image.blit(self.framesright[self.frameindex], (0,0))

            if self.shootcounter <= 0:
                #Shoot
                if self.targetingtriangle.spriteinside(playerx,playery):
                    if self.movingleft:
                        map.addprojectile(EnemyProjectileDiagonal(self.rect.x -5, self.rect.y - self.height, 20,20,45))
                    else:
                        map.addprojectile(EnemyProjectileDiagonal(self.rect.x + self.width, self.rect.y - self.height, 20,20,45,True))
                self.shootcounter = 20
            else:
                #Control rate of fire
                self.shootcounter -= 1


class Kamakazie(Collidable):
    def __init__(self, posx, posy, width, height):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 0
        self.shootcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable=True
        self.points = 30
        self.strength = 2
        self.frameindex = 0
        self.deathcount = 0
        #For targeting the player
        self.targety = None
        self.kamakazie = False

        #load images
        self.frames = [pygame.image.load(get_file_path("i","boagkama" + "/boagkama" + str(n) + ".png")) for n in range(14)]
        self.deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(18)]

    def move(self,**kwargs):
        playery = kwargs["playery"]
        playerx = kwargs["playerx"]
        if self.kamakazie:
            maxframe = 13
        else:
            maxframe = 8
        if self.frameindex < maxframe:
            self.frameindex += 1
        else:
            self.frameindex = 0
        #Need to move to the same level as the player and then shoot off
        if self.rect.y in range(playery-5,kwargs["playery"]+5) and self.rect.x - playerx < 400 and not self.kamakazie:
            #Target the player craft
            self.kamakazie = True
            self.vel = 8
        else:
            #move in direction of player
            #The ranges stops the jitter effect
            if self.rect.y not in range(playery-5,playery+5):
                if self.rect.y > playery:
                    self.rect.y -= 2
                else:
                    self.rect.y += 2
        #Death sequence
        if self.dead:
            self.rect.x = self.rect.x - self.vel
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.fill((255,255,255))
            if self.deathcount < 4:
                self.image.blit(self.frames[self.frameindex], (0,0))
            self.image.blit(self.deathSeq[self.deathcount],(0,0))
            if self.deathcount < 17:
                self.deathcount += 1
            else:
                #Set flag for removal
                self.remove = True
        else:
            self.image.blit(self.frames[self.frameindex], (0,0))
            self.rect.x -= self.vel



class HomingMissile(Collidable):
    def __init__(self, posx, posy, width, height, enemy=None):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 2
        self.shootcounter = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.destructable=True
        self.points = 30
        self.strength = 2
        self.frameindex = 0
        self.deathcount = 0
        #For targeting the player
        self.targety = None
        self.kamakazie = False
        self.movingright = False
        self.rotatingright = False
        self.rotatingleft = False
        self.rotatecount = 6
        self.completedrotation = False
        #If the player evades the missile long enough it self destructs
        self.giveupcount = 0
        #The enemy the missile is attached to
        self.enemy = enemy

        #load images
        self.frames = [pygame.image.load(get_file_path("i","homingmissile" + "/homingm" + str(n) + ".png")) for n in range(14)]
        self.deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(18)]

    def move(self,**kwargs):
        playery = kwargs["playery"]
        playerx = kwargs["playerx"]

        #Initial movement
        if self.kamakazie:
            maxframe = 13
            self.giveupcount += 1
            if self.giveupcount == 200:
                #Missile self destructs
                self.dead = True
        else:
            maxframe = 8
        if self.frameindex < maxframe:
            self.frameindex += 1
        else:
            self.frameindex = 0

        if self.enemy:
            #Missle is attached to enemy craft - move with the enemy
            self.image.fill((255,255,255))
            self.image.blit(self.frames[self.frameindex], (0,0))
            if self.enemy.launched:
                print("Launched")
                self.enemy.vel = 0
                self.rect.x -= self.vel
                self.rect.y = self.enemy.rect.y + self.enemy.missileyoffset
                #Detach once launched
                if self.rect.x < self.enemy.rect.x - self.enemy.width:
                    self.enemy = None
            else:
                self.rect.x = self.enemy.rect.x + self.enemy.missilexoffset
                self.rect.y = self.enemy.rect.y + self.enemy.missileyoffset

        else:
            #Need to move to the same level as the player and then shoot off
            if self.rect.y in range(playery-5,kwargs["playery"]+5) and self.rect.x - playerx < 400 and not self.kamakazie:
                #Target the player craft
                self.kamakazie = True
                self.vel = 8
            else:
                #move in direction of player
                #The ranges stops the jitter effect
                if self.rect.y not in range(playery-5,playery+5):
                    if self.rect.y > playery:
                        self.rect.y -= 2
                    else:
                        self.rect.y += 2
            #The missile passes the player
            if self.rect.x < playerx - 100:
                if not self.movingright:
                    self.movingright = True
                    self.rotatingright = True
            elif self.rect.x > playerx + 100:
                if self.movingright:
                    self.movingright = False
                    self.rotatingleft = True
            if self.movingright:
                if self.rotatingright:
                    if self.rotatecount >= 180:
                        #Finish rotation and move in direction
                        self.rotatingright = False
                    else:
                        self.image = pygame.transform.scale(self.image,(40,40))
                        self.image.fill((255,255,255))
                        self.image.blit(pygame.transform.rotate(self.frames[self.frameindex],self.rotatecount*-1), (0,0))
                        self.rotatecount += 6
                else:
                    #Turn back
                    self.image.fill((255,255,255))
                    self.image.blit(pygame.transform.flip(self.frames[self.frameindex],True,False), (0,0))
                    self.rect.x += self.vel
                    self.rotatecount = 6
            else:
                if self.rotatingleft:
                    if self.rotatecount >= 180:
                        #Finish rotation and move in direction
                        self.rotatingleft = False
                    else:
                        self.image = pygame.transform.scale(self.image,(40,40))
                        self.image.fill((255,255,255))
                        self.image.blit(pygame.transform.rotate(self.frames[self.frameindex],180 - self.rotatecount), (0,0))
                        self.rotatecount += 6
                else:
                    self.image.fill((255,255,255))
                    self.image.blit(self.frames[self.frameindex], (0,0))
                    self.rect.x -= self.vel
                    self.completedrotation = True
                    self.rotatecount = 6
            #Death sequence
            if self.dead:
                self.rect.x = self.rect.x - self.vel
                self.image = pygame.transform.scale(self.image,(50,50))
                self.image.fill((255,255,255))
                if self.deathcount < 4:
                    self.image.blit(self.frames[self.frameindex], (0,0))
                self.image.blit(self.deathSeq[self.deathcount],(0,0))
                if self.deathcount < 17:
                    self.deathcount += 1
                else:
                    #Set flag for removal
                    self.remove = True



class BoagPulse(Collidable):

    def __init__(self, posx, posy, width, height, movingdown, wave=False, group=False):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 3
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.movingdown=movingdown
        self.destructable=True
        self.points = 20
        self.strength = 1
        self.frameindex = 0
        self.deathcount = 0
        self.group = group
        #For wave movement pattern
        self.wave = wave
        if movingdown:
            self.miny = posy
            self.maxy = posy + (height * 4)
        else:
            self.miny = posy - (height * 4)
            self.maxy = posy
        #load images
        self.frames = [pygame.image.load(get_file_path("i","boagpulse" + "/boagpulse" + str(n) + ".png")) for n in range(15)]
        self.deathSeq = [pygame.image.load(get_file_path("i","explosion" + "/explosion" + str(n) + ".png")) for n in range(18)]

        self.image.blit(self.frames[self.frameindex], (0,0))

    def move(self,**kwargs):
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

        if self.frameindex < 14:
            self.frameindex += 1
        else:
            self.frameindex = 0
        if self.dead:
            self.rect.x = self.rect.x - self.vel
            self.image = pygame.transform.scale(self.image,(50,50))
            self.image.fill((255,255,255))
            if self.deathcount < 4:
                self.image.blit(self.frames[self.frameindex], (0,0))
            self.image.blit(self.deathSeq[self.deathcount],(-10,-10))
            if self.deathcount < 9:
                self.deathcount += 1
            else:
                #Set flag for removal
                self.remove = True
        else:
            #Control wave movement
            if self.wave:
                if self.movingdown:
                    self.rect.y += 10
                    if self.rect.y >= self.maxy:
                        self.movingdown = False
                else:
                    self.rect.y -= 10
                    if self.rect.y <= self.miny:
                        self.movingdown = True
            self.rect.x = self.rect.x - self.vel
            self.image.blit(self.frames[self.frameindex], (0,0))


class Atom(Collidable):

    def __init__(self, posx, posy, width, height,type="N"):
        Collidable.__init__(self,posx,posy,width,height,True)
        self.vel = 0
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.type = type
        self.movingdown=False
        self.movingup = False
        self.movingright=False
        self.movingleft = False
        self.destructable=True
        self.points = 10
        self.strength = 1
        self.frameindex = 0
        self.deathcount = 0
        #Change count for deciding when to change behaviour
        self.changecount = 0
        #For splitting
        self.reproduced = False


        #load images
        if type=="N":
            self.frames = [pygame.image.load(get_file_path("i","boagatom" + "/atom" + str(n) + ".png")) for n in range(19)]
            self.deathSeq = [pygame.image.load(get_file_path("i","atomsplit" + "/atomsplit" + str(n) + ".png")) for n in range(20)]
            self.deathlimit = 19
            self.framelimit = 14
        elif type=="R":
            self.frames = [pygame.image.load(get_file_path("i","boagatom2" + "/atom2" + str(n) + ".png")) for n in range(24)]
            self.deathSeq = [pygame.image.load(get_file_path("i","atomexplode" + "/atomexplode" + str(n) + ".png")) for n in range(11)]
            self.deathlimit = 10
            self.framelimit = 23
        elif type=="Y":
            self.frames = [pygame.image.load(get_file_path("i","boagatom3" + "/atom3" + str(n) + ".png")) for n in range(24)]
            self.deathSeq = [pygame.image.load(get_file_path("i","atomexplode" + "/atomexplode" + str(n) + ".png")) for n in range(11)]
            self.deathlimit = 10
            self.framelimit = 23
        elif type=="P":
            self.frames = [pygame.image.load(get_file_path("i","boagatom4" + "/atom4" + str(n) + ".png")) for n in range(24)]
            self.deathSeq = [pygame.image.load(get_file_path("i","atomexplode" + "/atomexplode" + str(n) + ".png")) for n in range(11)]
            self.deathlimit = 10
            self.framelimit = 23
    def move(self,**kwargs):
        map = kwargs["map"]

        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

        if self.frameindex < self.framelimit:
            self.frameindex += 1
        else:
            self.frameindex = 0
        if self.dead:
            if self.deathcount < self.deathlimit:
                self.image.blit(self.deathSeq[self.deathcount], (0,0))
                self.deathcount += 1
            else:
                ## NOTE: Don't know why this gets called twice, had to add the reproduced variable to control it
                self.remove = True
                if not self.reproduced and self.type == "N":
                    map.addenemy(Atom(self.rect.x,self.rect.y+self.height+10,25,25,"R"))
                    map.addenemy(Atom(self.rect.x,self.rect.y-self.height-10,25,25,"Y"))
                    self.reproduced = True
        else:
            self.image.blit(self.frames[self.frameindex], (0,0))
        #Decide behaviour
        if self.changecount == 0:
            if randrange(2) == 1:
                self.movingdown = True
            else:
                self.movingdown = False
            if randrange(2) == 1:
                self.movingright = True
            else:
                self.movingright = False
            if randrange(2) == 1:
                self.movingleft = True
            else:
                self.movingleft = False
            if randrange(2) == 1:
                self.movingup = True
            else:
                self.movingup = False
            self.vel = randrange(4)
            self.changecount = 40
        else:
            self.changecount -= 1
        if self.movingup and not self.movingdown:
            self.rect.y = self.rect.y - self.vel
        if self.movingdown and not self.movingup:
            self.rect.y = self.rect.y + self.vel
        if self.movingright and not self.movingleft:
            self.rect.x = self.rect.x + self.vel
        if self.movingleft and not self.movingright:
            self.rect.x = self.rect.x - self.vel

    """
    def hit(self,hitval,**kwargs):
        self.strength -= hitval
        if self.strength <=0:
            self.dead = True
            """







class EnemyGroup():
    def __init__(self, posx, posy, height):
        self.enemies = []
        self.x = posx
        self.y = posy
        self.startpos = posy
        self.endpos = posy + ( 30 * (height-1))

    def move(self,**kwargs):
        pass

    def onscreen(self,xoffset,screen):
        #Caculate object within screen area
        screenend = screen["w"] + xoffset
        onscreen = False
        for e in self.enemies:
            if e.rect.x  + e.rect.width > xoffset and e.rect.x < screenend:
                onscreen = True
        return onscreen


class ScobotGroup(EnemyGroup):
    def __init__(self, posx, posy, height):
        EnemyGroup.__init__(self,posx,posy,height)
        self.enemies.append(Scobot(self.x,self.y,20,30,False,True))
        self.movecount = 5

        for i in range(height-1):
            self.x = self.x + 25
            self.y = self.y + 30
            self.enemies.append(Scobot(self.x,self.y,20,30,False,True))
        #go backwards
        for i in range(height-1):
            self.x = self.x + 25
            self.y = self.y - 30
            self.enemies.append(Scobot(self.x,self.y,20,30,True,True))



    def draw(self,view):
        for s in self.enemies:
            s.draw(view)

    def move(self,**kwargs):
        #Move count controls the speed it animates at
        if self.movecount == 0:
            for s in self.enemies:
                if s.rect.y == self.startpos:
                    s.rect.y += 5
                    s.movingdown = True
                elif s.rect.y == self.endpos:
                    s.rect.y -= 5
                    s.movingdown = False
                else:
                    if s.movingdown:
                        s.rect.y += 5
                    else:
                        s.rect.y -= 5
            self.movecount = 5
        else:
            self.movecount -= 1



class ScobotWall(EnemyGroup):
    def __init__(self, posx, posy, height):
        EnemyGroup.__init__(self,posx,posy,height)
        self.enemies.append(Scobot(self.x,self.y,20,30,False,True))

        for i in range(height-1):
            self.y = self.y + 30
            self.enemies.append(Scobot(self.x,self.y,20,30,False,True))



class BoagPulseGroup(EnemyGroup):
    def __init__(self, posx, posy, width, wave=False):
        EnemyGroup.__init__(self,posx,posy,2)
        #self.enemies.append(Scobot(self.x,self.y,20,30,False))
        #self.movecount = 5
        self.startpos = posy
        self.endpos = posy + 70
        #Controls the space between the sprites
        self.gap = 0
        #self.movecount = 0

        for i in range(0,width):
            ## NOTE: Need to try to get a gap between the enemies
            #Up boagpulse
            self.enemies.append(BoagPulse(posx + self.gap + (60 * i),posy,30,30,False,wave,True))
            #Down boagpulse
            self.gap += 20
            self.enemies.append(BoagPulse(posx + self.gap + 30 + (60 * i),posy + 70,30,30,False,wave,True))
            self.gap += 20

    def move(self,**kwargs):
        #Move count controls the speed it animates at
        for s in self.enemies:
            if s.rect.y == self.startpos:
                s.rect.y += 5
                s.movingdown = True
            elif s.rect.y == self.endpos:
                s.rect.y -= 5
                s.movingdown = False
            else:
                if s.movingdown:
                    s.rect.y += 5
                else:
                    s.rect.y -= 5
