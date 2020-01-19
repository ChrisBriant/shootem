from include import get_file_path, collideontop
import pygame, os

class Enemy(pygame.sprite.Sprite):

    def __init__(self, platform, width, height, imagepath):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))

        self.x = platform.rect.x
        self.y = platform.rect.y - height
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.width = width
        self.height = height
        self.end = platform.rect.x + platform.width - self.width
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        #self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        #self.myhitbox = pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        #self.score = 0
        self.walkLeft = [pygame.image.load(get_file_path("i",imagepath + "/EL0.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/EL1.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/EL2.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/EL3.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/EL4.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/EL5.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/EL6.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/EL7.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/EL8.png"))]
        self.walkRight = [pygame.image.load(get_file_path("i",imagepath + "/ER0.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/ER1.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/ER2.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/ER3.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/ER4.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/ER5.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/ER6.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/ER7.png")),
                    pygame.image.load(get_file_path("i",imagepath + "/ER8.png"))]

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

    def move(self):
        if self.vel > 0:
            #going right
            if  self.rect.x < self.path[1] + self.vel:
                self.rect.x += self.vel
            else:
                self.vel = self.vel * -1
                self.rect.x += self.vel
                self.walkCount = 0
        else:
            if self.rect.x > self.path[0] - self.vel:
                # If we have not reached the furthest left point on our path
                self.rect.x += self.vel
            else:
                self.vel = self.vel * -1
                self.rect.x += self.vel
                self.walkCount = 0


    def hit(self):
        print(hit)
