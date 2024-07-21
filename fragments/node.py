import pygame
from engine import Color

class Node:
    def __init__(self, position, intensity=0):
        self.x, self.y, self.z = position
        self.intensity = 0
        self

    def update(self, nodes):
        self.state = self.position.update(nodes)

    def draw(self, screen, circle_rad):
        pygame.draw.circle(screen, Color.fromNodeIntensity(self.intensity).val(), self.position.xy, circle_rad)
