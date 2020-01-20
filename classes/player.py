from include import get_file_path, collideontop
import pygame, os

class Player(pygame.sprite.Sprite):
    walkRight = [pygame.image.load(get_file_path("i","R1.png")),
                pygame.image.load(get_file_path("i","R2.png")),
                pygame.image.load(get_file_path("i","R3.png")),
                pygame.image.load(get_file_path("i","R4.png")),
                pygame.image.load(get_file_path("i","R5.png")),
                pygame.image.load(get_file_path("i","R6.png")),
                pygame.image.load(get_file_path("i","R7.png")),
                pygame.image.load(get_file_path("i","R8.png")),
                pygame.image.load(get_file_path("i","R9.png"))]
    walkLeft = [pygame.image.load(get_file_path("i","L1.png")),
                pygame.image.load(get_file_path("i","L2.png")),
                pygame.image.load(get_file_path("i","L3.png")),
                pygame.image.load(get_file_path("i","L4.png")),
                pygame.image.load(get_file_path("i","L5.png")),
                pygame.image.load(get_file_path("i","L6.png")),
                pygame.image.load(get_file_path("i","L7.png")),
                pygame.image.load(get_file_path("i","L8.png")),
                pygame.image.load(get_file_path("i","L9.png"))]
    deathSeq = [pygame.image.load(get_file_path("i","D1.png")),
                pygame.image.load(get_file_path("i","D2.png")),
                pygame.image.load(get_file_path("i","D3.png")),
                pygame.image.load(get_file_path("i","D4.png")),
                pygame.image.load(get_file_path("i","D5.png")),
                pygame.image.load(get_file_path("i","D6.png")),
                pygame.image.load(get_file_path("i","D7.png")),
                pygame.image.load(get_file_path("i","D8.png")),
                pygame.image.load(get_file_path("i","D9.png"))]
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


    def hit(self):
        print("Hit Goblin!")

    def draw(self, view):
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

        if self.walkCount + 1 > 9:
            self.walkCount = 0

        if self.dead:
            #Animate death sequence
            #increase image size first
            self.image = pygame.transform.scale(self.image,(40,50))
            self.image.fill((255,255,255))
            self.image.set_colorkey((255,255,255))
            self.image.blit(self.deathSeq[self.deathCount], (0,0))
            if self.deathCount < 8:
                print(self.deathCount)
                self.deathCount += 1
        else:
            #Normal movement
            if not(self.standing):
                if self.left:
                    self.image.blit(self.walkLeft[self.walkCount], (0,0))
                    self.walkCount += 1
                elif self.right:
                    self.image.blit(self.walkRight[self.walkCount], (0,0))
                    self.walkCount +=1
            else:
                if self.right:
                    self.image.blit(self.walkRight[0], (0,0))
                else:
                    self.image.blit(self.walkLeft[0], (0,0))
        view.blit(self.image,(self.rect.x,self.rect.y))

    def moveleft(self):
        self.rect.x -= self.vel
        self.left = True
        self.right = False
        self.up = False
        self.down = False
        self.standing = False

    def moveright(self):
        self.rect.x += self.vel
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


    def moveplayer(self,keys,screen, gamearea):
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
            elif keys[pygame.K_RIGHT] and self.rect.x < gamearea["w"] - self.width:
                self.moveright()
            elif keys[pygame.K_UP] and self.rect.y > 0:
                self.moveup()
            elif keys[pygame.K_DOWN] and self.rect.y < gamearea["h"] - self.height:
                self.movedown()
            else:
                self.standing = True
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
        print(xoffset, ",",self.rect.x)
        if self.rect.x < xoffset:
            return True
        else:
            return False

    #Routine for player death
    def die(self):
        if not self.dead:
            self.dead = True
            self.lives -= 1
            self.deathpos = (self.rect.x,self.rect.y)
            print("Hit!")
