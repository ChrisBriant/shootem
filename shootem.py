from classes.player import Player
#from classes.collidables import Collidable, Wall, Floor1
from classes.scoreboard import ScoreBoard
#from classes.gamemap import GameMap
from classes.levels import Level
from classes.screenmessage import OnScreenMessage, FlashingText
import pygame, os,math

pygame.init()

clock = pygame.time.Clock()

def redrawGameWindow(totalscore):
    view.fill((0,0,0))
    view.blit(level.bg,(0 - xoffset,0-yoffset))

    if ship.dead and ship.lives <= 0:
        ship.draw(view)
        gameover.draw(view,xoffset,yoffset,screen)
    elif level.leveltrans:
        #Level transition screen
        level.levelovermessage.draw(view,xoffset,yoffset,screen)
        level.enemieskilled.draw(view,0,50,xoffset,yoffset,screen)
        if level.enemieskilled.done:
            level.bonus.draw(view,0,90,xoffset,yoffset,screen)
            level.scoretext.draw(view,0,130,xoffset,yoffset,screen)
        pressanykey.draw(view,0,170,xoffset,yoffset,screen)
    else:
        if ship.dead:
            ship.draw(view)
            deathmessage.draw(view,xoffset,yoffset,screen)
            pressanykey.draw(view,0,100,xoffset,yoffset,screen)
        else:
            ship.draw(view)
            onscreensprites = map.getcollidables(xoffset)
            onscreensprites.draw(view)
            map.updatecollidables(onscreensprites,level=level)
    view.blit(map.scoreboard.getsurface(),(xoffset*-1,0))
    win.blit(view,(xoffset,yoffset))

    pygame.display.update()

screen = { "w":1000, "h":600 }
#gamearea = {"w":4000,"h":600 }

win = pygame.display.set_mode((screen["w"],screen["h"]))
pygame.display.set_caption("First Game")


#xplayerstartpos = 200
#yplayerstartpos = 100
ship = Player(0, 0, 60,30)

#Messages
deathmessage = OnScreenMessage(70,"YOU DIED!")
gameover = OnScreenMessage(70,"GAME OVER!")
pressanykey = FlashingText(26,"Press any key to continue")


#Create Level
level = Level(ship,screen)
level.loadlevel(1)
map = level.map
gamearea = level.gamearea
#The view containing all of the objects
view = pygame.Surface((gamearea["w"],gamearea["h"]))

run = True
totalscore = 0
xoffset = ship.calculatexoffset(screen,gamearea)
yoffset = ship.calculateyoffset(screen,gamearea)
win.blit(view, (0,0))
ship.draw(win)
#mainloop

while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()

    #Transition to next level if key pressed
    if level.leveltrans and keys[pygame.K_SPACE]:
        map.scoreboard.addscore(level.bonusval)
        level.leveltrans = False

    #Move player if up, left, or right keys pressed
    if not level.leveltrans:
        ship.moveplayer(keys, screen, gamearea, map,xoffset*-1)
    redrawGameWindow(0)
    #Detect collidion
    if map.collision():
        ship.die(map,xoffset)
    #Ship collides with the left of the screen
    if ship.catchscreen(xoffset):
        ship.die(map,xoffset)
    #For side scrolling
    if xoffset > 0 - (gamearea["w"]-screen["w"]):
        xoffset -= 1
    #Reset offset if on new level
    if ship.newlevel and not level.leveltrans:
        xoffset = 0
        oldscoreboard = map.scoreboard
        map = level.map
        map.scoreboard = oldscoreboard
        map.scoreboard.level = level.levelno
        ship.newlevel = False

    #Detect collision between ship and enemies

    #If dead then pressing space re-starts game
    if ship.dead:
        #Create new instance of ship -overwrite current instance
        if keys[pygame.K_SPACE]:
            lives = map.scoreboard.lives
            deathpos = list(ship.deathpos)
            map.player = Player(deathpos[0], deathpos[1], 60,30,lives)
            ship = map.player

pygame.quit()
