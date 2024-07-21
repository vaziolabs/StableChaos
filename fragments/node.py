import pygame
from engine import Color
from .settings import Settings

class Node:
    def __init__(self, position, intensity=0.5):
        self.x, self.y, self.z = position
        self.intensity = intensity
        self.radius = Settings.NODE_SIZE.value

    def update(self, nodes):
        self.state = self.position.update(nodes)

    # TODO: Build a 'blit' method that will translate from XYZ to XY
    def position(self):
        return (self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, Color.fromNodeIntensity(self.intensity), self.position(), self.radius)
