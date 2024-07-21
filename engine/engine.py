import pygame
from pygame.locals import *
from .color import Color
import sys

class Engine:
    def __init__(self, screen_size):
        self.screen_size = screen_size

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Hybrid Abstract Transitory Structure")
        self.background = pygame.Surface(screen_size).convert()
        self.background.fill(Color.BLACK_FILL.val())
        self.clock = pygame.time.Clock()

    def run(self, fn):
        print("Running Engine")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # resize
                if event.type == VIDEORESIZE or (event.type == KEYDOWN and event.key == K_r):
                    self.screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                    self.background = pygame.Surface(self.screen.get_size())
                    self.background = self.background.convert()
                    self.background.fill(Color.WHITE_BACKGROUND.val())
                

            # Pass In The Logic to be Executed in the Main Loop
            self.screen.blit(self.background, (0, 0))
            fn()
            pygame.display.flip()
            self.clock.tick(15)
