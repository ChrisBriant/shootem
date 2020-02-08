from classes.player import Player
from classes.collidables import Collidable, Wall, Floor1
from classes.scoreboard import ScoreBoard
from classes.gamemap import GameMap
from classes.screenmessage import OnScreenMessage
import pygame, os,math

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

clock = pygame.time.Clock()

def redrawGameWindow(totalscore):
    view.fill((0,0,0))

    if ship.dead and ship.lives <= 0:
        print("Here")
        ship.draw(view)
        gameover.draw(view,xoffset,yoffset,screen)
    else:
        if ship.dead:
            ship.draw(view)
            deathmessage.draw(view,xoffset,yoffset,screen)
        else:
            ship.draw(view)
            onscreensprites = map.getcollidables(xoffset)
            onscreensprites.draw(view)
            map.updatecollidables(onscreensprites)
    view.blit(map.scoreboard.getsurface(),(xoffset*-1,0))
    win.blit(view,(xoffset,yoffset))

    pygame.display.update()


xplayerstartpos = 200
yplayerstartpos = 100
ship = Player(xplayerstartpos, yplayerstartpos, 60,30)

#Messages
deathmessage = OnScreenMessage(70,"YOU DIED!")
gameover = OnScreenMessage(70,"GAME OVER!")


#Create Level
map = GameMap(gamearea,screen, ship)

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

    #Move player if up, left, or right keys pressed
    ship.moveplayer(keys, screen, gamearea, map)
    redrawGameWindow(0)
    #Detect collidion
    if map.collision():
        ship.die(map,xoffset)
    #Ship collides with the left of the screen
    if ship.catchscreen(xoffset):
        ship.die(map,xoffset)
    #For side scrolling
    if xoffset > 0 - (gamearea["w"] / 2):
        xoffset -= 1

    #Detect collision between ship and enemies

    #If dead then pressing space re-starts game
    if ship.dead:
        #Create new instance of ship -overwrite current instance
        if keys[pygame.K_SPACE]:
            lives = map.scoreboard.lives
            deathpos = list(ship.deathpos)
            ship = Player(deathpos[0], deathpos[1], 60,30,lives)

pygame.quit()
