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
            
    def acumen(self):
        init_color = Color.WHITE_FILL.val()
        min_r, min_g, min_b = init_color
        max_r, max_g, max_b = Color.BLACK_FILL.val()

        for node in self.nodes:
            r, g, b = Color.fromState(node.state)
            print("comparing", r, g, b)
            min_r = min(min_r, r)
            min_g = min(min_g, g)
            min_b = min(min_b, b)
            max_r = max(max_r, r)
            max_g = max(max_g, g)
            max_b = max(max_b, b)

        r, g, b = (lerp(min_r, max_r, 0.5), lerp(min_g, max_g, 0.5), lerp(min_b, max_b, 0.5))
        new_r = (lerp(self.prev_r, r, 0.5) + 128) // 2
        new_g = (lerp(self.prev_g, g, 0.5) + 128) // 2
        new_b = (lerp(self.prev_b, b, 0.5) + 128) // 2
        new_rgb = (new_r, new_g, new_b)
        self.prev_r, self.prev_g, self.prev_b = new_rgb
        return new_rgb


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

            # We draw a bigger circle to encompass all the nodes
            circle_rad = self.screen_size[0] // 2 if self.screen_size[0] < self.screen_size[1] else self.screen_size[1] // 2.2
            pygame.draw.circle(self.screen, self.acumen(), (800, 600), circle_rad)

            self.calculateNodeValues()
            self.drawNodes()

            pygame.display.flip()
            self.clock.tick(30)