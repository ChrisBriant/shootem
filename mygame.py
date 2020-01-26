from classes.player import Player
from classes.enemy import Rocket, Scobot, ScobotGroup, BoagGunship
from classes.collidables import Collidable
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
char = pygame.image.load(get_file_path("i","standing.png"))


clock = pygame.time.Clock()

"""
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface((width, height))
       self.image.fill((255,0,0))
       #self.image.blit(self.walkRight[0],(0,0))
       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.width = width
       self.height = height
"""





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
yplayerstartpos = 0
ship = Player(xplayerstartpos, yplayerstartpos, 60,30)

"""
platform1 = Platform(100,50,60,20)
platform2 = Platform(200,150,100,20)
platform3 = Platform(350,420,100,20)
platform4 = Platform(600,420,100,20)
platform5 = Platform(990,420,200,20)
platform6 = Platform(100,600,100,20)
platform7 = Platform(100,980,100,20)
platform8 = Platform(1400,940,100,20)
platform9 = Platform(1200,880,100,20)
platform10 = Platform(1400,820,100,20)
platform11 = Platform(1200,740,100,20)
platform12 = Platform(1400,720,100,20)
platform13 = Platform(1200,680,100,20)
platform14 = Platform(1400,640,100,20)
platform15 = Platform(1200,600,100,20)
platform16 = Platform(1400,560,100,20)
platform17 = Platform(1200,520,100,20)
platform18 = Platform(1400,480,100,20)
platform19 = Platform(1200,440,100,20)
platform20 = Platform(1400,400,100,20)
platform21 = Platform(1200,380,100,20)
platform22 = Platform(1400,340,100,20)
platform23 = Platform(1200,300,100,20)
platform24 = Platform(1400,280,100,20)
platform25 = Platform(1200,240,100,20)
platform26 = Platform(1400,200,100,20)
platform27 = Platform(1200,160,100,20)
platform28 = Platform(1400,120,100,20)
platform29 = Platform(1000,80,200,20)
platform30 = Platform(1400,40,100,20)
platform31 = Platform(1200,0,100,20)
platform32 = Platform(600,960,800,20)
"""




#Enemys
#alien1 = Enemy(platform32, 32, 32, "alien1")

#Messages
deathmessage = OnScreenMessage(70,"YOU DIED!")

"""
platformgroup = pygame.sprite.Group(platform1,platform2,platform3,platform4,platform5,platform6,platform7,platform8,
                                        platform9,platform10,platform11,platform12,platform13,platform14,platform15,
                                        platform16,platform17,platform18,platform19,platform20,platform21,platform22,
                                        platform23,platform24,platform25,platform26,platform27,platform28,platform29,
                                        platform30,platform31,platform32)
"""


#Create Level
map = GameMap(gamearea,screen, ship)
map.addcollidable(100,100,100,100)
map.addcollidable(1500,200,100,100)
map.addcollidable(1600,400,100,100)
map.addenemy(Rocket(800,540,30,60))
map.addenemy(Rocket(1400,540,30,60))
map.addenemy(BoagGunship(800,300,60,40))
"""
map.addenemy(Scobot(400,100,20,30))
map.addenemy(Scobot(600,200,20,30))
map.addenemy(Scobot(1000,100,20,30))
map.addenemy(Scobot(1200,200,20,30))
map.addenemy(Scobot(1200,400,20,30))
map.addenemy(Scobot(1200,450,20,30))
"""
#map.addenemygroup(ScobotGroup(800,300,5))
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
