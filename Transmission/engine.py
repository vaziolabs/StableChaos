from copy import deepcopy
import pygame
from pygame.locals import *
from color import Color

import sys

def lerp(c_A, c_B, t):
    t = (t + 2.0) / 4.0 # This value is potentially -2 to 2
    return int(c_A + (c_B - c_A) * t)

# Define Pygame Engine class
class Engine:
    def __init__(self, screen_size, nodes):
        self.nodes = nodes
        self.screen_size = screen_size
        self.prev_r = 0
        self.prev_g = 0
        self.prev_b = 0

        # Initialize Pygame
        pygame.init()
        
        # Set the screen size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Hybrid Abstract Transitory Structure")
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Color.WHITE_BACKGROUND.val())
        self.clock = pygame.time.Clock()
            

    def drawConnections(self):
        # Draw the nodes
        for node in self.nodes:
            node.draw(self.screen)

    def calculateNodeValues(self):
        # TODO: Integrate N node-transmission receivers
        return

    # Main loop
    def run(self):
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

            # Draw the background
            self.screen.blit(self.background, (0, 0))

            # We draw a bigger circle to encompass all the nodes
            circle_rad = self.screen_size[0] // 2 if self.screen_size[0] < self.screen_size[1] else self.screen_size[1] // 2.2
            pygame.draw.circle(self.screen, self.acumen(), (800, 600), circle_rad)

            self.calculateNodeValues()
            self.drawNodes()

            pygame.display.flip()
            self.clock.tick(30)