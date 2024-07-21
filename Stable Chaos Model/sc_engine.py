from copy import deepcopy
import pygame
import sys
sys.path.append('../')
from engine import Engine, Color

import sys

def lerp(c_A, c_B, t):
    t = (t + 2.0) / 4.0 # This value is potentially -2 to 2
    return int(c_A + (c_B - c_A) * t)

# Define Pygame Engine class
class SCEngine(Engine):
    def __init__(self, screen_size, nodes):
        super().__init__(screen_size, nodes)
        self.prev_r = 0
        self.prev_g = 0
        self.prev_b = 0
            
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


    def calculateNodeValues(self):
        new_nodes = []

        for node in self.nodes:
            new_node = deepcopy(node)
            new_node.update(self.nodes)
            new_nodes.append(new_node)

        self.nodes = new_nodes

    def cycle(self):
            # Draw the background
            self.screen.blit(self.background, (0, 0))

            # We draw a bigger circle to encompass all the nodes
            circle_rad = self.screen_size[0] // 2 if self.screen_size[0] < self.screen_size[1] else self.screen_size[1] // 2.2
            pygame.draw.circle(self.screen, self.acumen(), (600, 600), circle_rad)

            self.calculateNodeValues()
            self.drawNodes()

            pygame.display.flip()
            self.clock.tick(15)