import pygame
from color import Color
from state import State
import random

def OppositeNode(name):
    if name == "A":
        return "D"
    elif name == "B":
        return "C"
    elif name == "C":
        return "B"
    elif name == "D":
        return "A"

def LeftNeighbor(name):
    if name == "A":
        return "B"
    elif name == "B":
        return "C"
    elif name == "C":
        return "D"
    elif name == "D":
        return "A"
    
def RightNeighbor(name):
    if name == "A":
        return "D"
    elif name == "B":
        return "A"
    elif name == "C":
        return "B"
    elif name == "D":
        return "C"

class Node:
    def __init__(self, position, color):
        self.position = position
        self.name = "A" if position.idx == 0 else "B" if position.idx == 1 else "C" if position.idx == 2 else "D"
        self.color = color
        self.radius = 50
        self.outline = 2
        self.randomA = random.uniform(-1.0, 1.0)
        self.randomB = random.uniform(-1.0, 1.0)
        self.state = State(self.randomA, self.randomB)

    def draw (self, screen):
        pygame.draw.circle(screen, Color.BLACK_OUTLINE.value, (self.position.x, self.position.y), self.radius + self.outline)
        pygame.draw.circle(screen, Color.fromState(self.state), (self.position.x, self.position.y), self.radius)

    def calculateNewRandomness(self):
        # Choose a random value between -1 and 1
        self.randomA = random.randint(-1, 1)
        self.randomB = random.randint(-1, 1)

    def update(self, nodes):
        self.calculateNewRandomness()

        for node in nodes:
            if node.name == self.name:
                continue

            # If we have the opposite node, we want to do the opposite of what it does
            if self.name is OppositeNode(node.name):
                self.state.repel(node.state)
                return
            
            # If we have a double 0, we want to do nothing
            if self.randomA == 0 and self.randomB == 0:
                return

            if self.randomA > 0 and self.randomB > 0:
                # If we have a double positive, we want to attempt to move away from our neighbor
                self.state.minusA()
                self.state.minusB()
                return
            elif self.randomA < 0 and self.randomB < 0:
                # If we have a double negative, we want to attempt to overtake or be like our neighbor
                self.state.addA()
                self.state.addB()
                return
            
            # Otherwise, we want to introduce some randomness to the node corresponding to our neighbor
            # TODO: Add a Gradient here
            if node.name is LeftNeighbor(self.name):
                # If we have a mix of positive and negative, we want to attempt to be like our neighbor in one way or another
                if self.randomA > 0.0: # If Random A is A Positive, we want to do LIKE our left neighbor in the A direction
                    if node.state.A < 1.0:
                        self.state.minusA()
                    if node.state.B > -1.0:
                        self.state.minusB()
                elif self.randomA < 0: 
                    if node.state.A > -1.0:
                        self.state.addA()
                    if node.state.B < 1.0:
                        self.state.addB()
                return
            
            if node.name is RightNeighbor(self.name):
                if self.randomB > 0.0: # If Random B is B Positive, we want to do LIKE our right neighbor in the B direction
                    if node.state.B > -1.0:
                        self.state.addB()
                    if node.state.A < 1.0:
                        self.state.addA()
                elif self.randomB < 0.0:
                    if node.state.B < 1.0:
                        self.state.minusB()
                    if node.state.A > -1.0:
                        self.state.minusA()
                return
