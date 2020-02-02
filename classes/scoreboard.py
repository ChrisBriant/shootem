from include import get_file_path
import pygame, os

class ScoreBoard():

    def __init__(self,screen,font="comicsans"):
        #Height of scoreboard is 8% of screen height
        self.height = screen["h"] / 100 * 8
        self.image = pygame.Surface((screen["w"],self.height))
        self.font = pygame.font.SysFont(font, 20, True)
        self.text = self.font.render("SCORE:", 1, (254,254,254))
        self.image.blit(self.text,(0,0))

    def getsurface(self):
        print(self.height)
        return self.image
