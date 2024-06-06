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

class Node:
    def __init__(self, position, color):
        self.position = position
        self.name = "A" if position.idx == 0 else "B" if position.idx == 1 else "C" if position.idx == 2 else "D"
        self.color = color
        self.radius = 50
        self.outline = 2
        self.randomA = random.randint(-1, 1)
        self.randomB = random.randint(-1, 1)
        self.state = State(self.randomA, self.randomB)

    def draw (self, screen):
        pygame.draw.circle(screen, Color.BLACK_OUTLINE.value, (self.position.x, self.position.y), self.radius + self.outline)
        pygame.draw.circle(screen, Color.fromState(self.state).value, (self.position.x, self.position.y), self.radius)

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
            # Otherwise, we want to introduce some randomness to the node corresponding to our neighbor
            else: # TODO: Add a Gradient here
                if self.randomA > 0 and self.randomB > 0:
                    # If we have a double positive, we want to attempt to overtake or be like our neighbor
                    if node.state.A < 1:
                        self.state.addA()
                    if node.state.B < 1:
                        self.state.addB()
                elif self.randomA < 0 and self.randomB < 0:
                    # If we have a double negative, we want to attempt to move away from our neighbor
                    if node.state.A > -1:
                        self.state.minusA()
                    if node.state.B > -1:
                        self.state.minusB()
                else:
                    # If we have a mix of positive and negative, we want to attempt to be like our neighbor in one way
                    if self.randomA > 0:
                        if node.state.A < 1:
                            self.state.addA()
                        if node.state.B > -1:
                            self.state.minusB()
                    elif self.randomB > 0:
                        if node.state.B < 1:
                            self.state.addB()
                        if node.state.A > -1:
                            self.state.minusA()
                    elif self.randomA < 0: # and if we are under the threshold we want to do the inverse
                        if node.state.A > -1:
                            self.state.minusA()
                        if node.state.B < 1:
                            self.state.addB()
                    elif self.randomB < 0:
                        if node.state.B > -1:
                            self.state.minusB()
                        if node.state.A < 1:
                            self.state.addA()
                # And if we have 0's we just want to maintain our current state
                # The problem with this model is that we could potentially do more than one operation, and we really want to calculate ALL possible operations before we do any of them