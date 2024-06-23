import pygame
from enum import Enum
from pygame.locals import *
import sys

class Color(Enum):
    BLACK_OUTLINE = (33, 33, 33)
    WHITE_BACKGROUND = (222, 222, 222)
    BLACK_FILL = (0, 0, 0)
    WHITE_FILL = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 128)

    def val(self):
        return self.value if isinstance(self.value, tuple) else self

    @staticmethod
    def lerp(color_A, color_B, t):
        t = (t + 1.0) / 2.0 # This value is originally -1 to 1

        color_A = color_A.value if isinstance(color_A, Color) else color_A
        color_B = color_B.value if isinstance(color_B, Color) else color_B

        r = int(color_A[0] + (color_B[0] - color_A[0]) * t)
        g = int(color_A[1] + (color_B[1] - color_A[1]) * t)
        b = int(color_A[2] + (color_B[2] - color_A[2]) * t)
        return (r, g, b)
    
    @staticmethod
    def fromPosition(i):
        if i == 0:
            return Color.RED
        elif i == 1:
            return Color.GREEN
        elif i == 2:
            return Color.BLUE
        else:
            return Color.WHITE_FILL
        
    @staticmethod
    def fromState(state):
        A_Color = Color.lerp(Color.WHITE_FILL, Color.BLUE, state.A)
        B_Color = Color.lerp(Color.BLACK_FILL, Color.RED, state.B)
        return Color.lerp(A_Color, B_Color, (state.A + state.B) / 2.0)

class Engine:
    def __init__(self, screen_size, nodes):
        self.nodes = nodes
        self.screen_size = screen_size

        # Initialize Pygame
        pygame.init()
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

    def run(self, fn):
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
            fn()