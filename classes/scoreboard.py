from include import get_file_path
import pygame, os

class ScoreBoard():

    def __init__(self,screen,lives,font="Arial"):
        #Height of scoreboard is 8% of screen height
        self.height = screen["h"] / 100 * 8
        self.livespos = int(screen["w"] / 100 * 75)
        self.image = pygame.Surface((screen["w"],self.height))
        self.font = pygame.font.SysFont(font, 30, True)
        self.score = 0
        self.lives = lives
        self.lifeimage = pygame.image.load(get_file_path("i","life.png"))

        #self.text = self.font.render("SCORE: " + str(self.score), 1, (254,254,254))
        #self.image.blit(self.text,(0,0))

    def getsurface(self):
        #Score
        self.image.fill((0,0,0))
        self.image.set_colorkey((255,255,255))
        self.text = self.font.render("SCORE: " + str(self.score), 1, (254,254,254))
        #Lives
        for i in range(self.lives):
            self.image.blit(self.lifeimage,(self.livespos+(i*34),0))
        self.image.blit(self.text,(0,0))
        return self.image

    def addscore(self,score):
        self.score += score

    def updatelives(self,lives):
        self.lives = lives
