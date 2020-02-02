from classes.player import Player
from classes.enemy import Rocket, Scobot, ScobotGroup, BoagGunship, BoagPulse, BoagPulseGroup, GunUpDown, \
    Kamakazie, HomingMissile, Atom
from classes.collidables import Collidable, Wall
from classes.scoreboard import ScoreBoard
from classes.gamemap import GameMap
from classes.screenmessage import OnScreenMessage
import pygame, os
pygame.init()

screen = { "w":1000, "h":600 }
gamearea = {"w":4000,"h":600 }

win = pygame.display.set_mode((screen["w"],screen["h"]))
view = pygame.Surface((gamearea["w"],gamearea["h"]))
pygame.display.set_caption("First Game")


#Get the filepath
def get_file_path(type,filename):
    if type == "i":
        return os.path.join("images", filename)

#Test collision of sprite on top of another
def collideontop(topsprite,bottomspritegrp):
    collision = False
    for sprite in bottomspritegrp.sprites():
        if (sprite.rect.x - topsprite.width) <= topsprite.rect.x <= (sprite.rect.x + sprite.width) \
            and (sprite.rect.y) <= topsprite.rect.y + topsprite.height <= (sprite.rect.y + sprite.height):
            collision = True
    return collision

bg = pygame.image.load(get_file_path("i","bg.jpg"))
#char = pygame.image.load(get_file_path("i","standing.png"))


clock = pygame.time.Clock()

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

def redrawGameWindow(totalscore):
    view.fill((0,0,0))

    if ship.dead:
        #alien1.draw(view)
        #platformgroup.draw(view)
        ship.draw(view)
        deathmessage.draw(view,xoffset,yoffset,screen)
    else:
        ship.draw(view)
        #alien1.draw(view)
        #platformgroup.draw(view)
        onscreensprites = map.getcollidables(xoffset)
        onscreensprites.draw(view)
        map.updatecollidables(onscreensprites)
    view.blit(map.scoreboard.getsurface(),(xoffset*-1,0))
    win.blit(view,(xoffset,yoffset))
    #goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    font = pygame.font.Font('freesansbold.ttf', 14)
    #text = font.render(str(totalscore), True, (0,255,0), (0,0,255))
    textsurface = font.render(str(totalscore), True, (0,0,0))
    textrect = textsurface.get_rect()
    #TextSurf, TextRect = text_objects(str(totalscore), font)
    textrect.center = ((20),(20))
    #textrect = pygame.draw.rect(win, (0,0,0), (10,10,100,100))
    win.blit(textsurface, textrect)
    pygame.display.update()


xplayerstartpos = 200
yplayerstartpos = 100
ship = Player(xplayerstartpos, yplayerstartpos, 60,30)




#Enemys
#alien1 = Enemy(platform32, 32, 32, "alien1")

#Messages
deathmessage = OnScreenMessage(70,"YOU DIED!")


#Create Level
map = GameMap(gamearea,screen, ship)
#map.addcollidable(100,100,100,100)
#map.addcollidable(1500,200,100,100)
#map.addcollidable(1600,400,100,100)
#map.addenemy(Rocket(800,540,30,60))
#map.addenemy(Rocket(1400,540,30,60))
#map.addenemy(BoagGunship(800,0,60,40))
#map.addenemy(BoagGunship(800,200,60,40))
map.addenemy(Scobot(900,100,20,30))
#map.addenemy(BoagPulse(800,300,30,30,True,True))
#map.addenemygroup(BoagPulseGroup(900,300,8,False))
#map.addenemy(GunUpDown(800,0,20,30))
#map.addenemy(GunUpDown(400,560,20,30,False))
#map.addenemy(Kamakazie(800,100,55,20))
#map.addenemy(HomingMissile(800,100,55,20))
#map.addenemy(Atom(800,100,25,25,"Y"))
#map.addenemy(Atom(800,100,25,25,"R"))
#map.addenemy(Atom(800,100,50,50))
#map.addcollidable(Wall(600,0,10))
map.addenemy(Scobot(900,200,20,30))
"""
map.addenemy(Scobot(400,100,20,30))
map.addenemy(Scobot(600,200,20,30))
map.addenemy(Scobot(1000,100,20,30))
map.addenemy(Scobot(1200,200,20,30))
map.addenemy(Scobot(1200,400,20,30))
map.addenemy(Scobot(1200,450,20,30))
"""
#scoreboard = ScoreBoard(gamearea)
#map.addenemygroup(ScobotGroup(1000,300,5))
#colidegroup = pygame.sprite.Group(collidable)

#group containing player and platforms
#platformsandplayer = pygame.sprite.Group(platform1, platform2, ship)
#enemies sprite group
#enemies = pygame.sprite.Group(alien1)
shootLoop = 0
bullets = []
run = True
totalscore = 0
xoffset = ship.calculatexoffset(screen,gamearea)
yoffset = ship.calculateyoffset(screen,gamearea)
win.blit(view, (0,0))
ship.draw(win)
#mainloop
while run:
    clock.tick(27)

    """
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
        """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    """
    for bullet in bullets:
        if  bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            """

    keys = pygame.key.get_pressed()

    #For shooting to be used later
    """
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if ship.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(projectile(round(ship.x + ship.width // 2), round(ship.y + ship.height // 2), 6, (0,0,0), facing))

        shootLoop = 1
        """
    #Move player if up, left, or right keys pressed
    ship.moveplayer(keys, screen, gamearea, map)
    redrawGameWindow(0)
    #Detect collidion
    if map.collision():
        ship.die()
    #Ship collides with the left of the screen
    if ship.catchscreen(xoffset):
        ship.die()
    #For scrolling
    #side scrolling
    if xoffset > 0 - (gamearea["w"] / 2):
        xoffset -= 1
    #xoffset = ship.calculatexoffset(screen,gamearea)
    #yoffset = ship.calculateyoffset(screen,gamearea)
    #Detect collision between ship and enemies

    #If dead then pressing space re-starts game
    if ship.dead:
        #Create new instance of ship -overwrite current instance
        print(ship.deathpos)
        if keys[pygame.K_SPACE]:
            lives = self.lives
            deathpos = list(ship.deathpos)
            ship = Player(deathpos[0], deathpos[1], 60,30,lives)
    #print(ship.rect.x,",", ship.rect.y," offset=", yoffset,"---", ship.calculateyoffset(screen,gamearea))

pygame.quit()
