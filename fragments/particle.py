import pygame 
from engine import  Color

magnitude = 1

class Particle:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def update(self, nodes):
        self.color = Color.fromState(self.position.state)
        self.position.update(nodes)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color.val(), self.position, 5)
