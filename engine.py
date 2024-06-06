from copy import deepcopy
import pygame
from pygame.locals import *
from color import Color

import sys

# Define Pygame Engine class
class Engine:
    def __init__(self, screen_size, nodes):
        self.nodes = nodes

        # Initialize Pygame
        pygame.init()
        
        # Set the screen size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Hybrid Abstract Transitory Structure")
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Color.WHITE_BACKGROUND.val())
        self.clock = pygame.time.Clock()

    def drawNodes(self):
        # Draw the nodes
        for node in self.nodes:
            node.draw(self.screen)

    def calculateNodeValues(self):
        new_nodes = []

        for node in self.nodes:
            new_node = deepcopy(node)
            new_node.update(self.nodes)
            new_nodes.append(new_node)

        self.nodes = new_nodes

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

            self.calculateNodeValues()

            # Draw the nodes
            self.drawNodes()

            # Update the screen
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(10)