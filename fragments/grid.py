from .node import Node
from .settings import Settings

grid_size = Settings.GRID_SIZE.value
total_nodes = grid_size ** 3

scalar = lambda scaled: scaled * Settings.NODE_SPACING.value + Settings.GRID_OFFSET.value
class Grid:
    def __init__(self):
        print("Creating Grid")
        self.nodes = []
        for x in range(grid_size): 
            for y in range(grid_size):
                for z in range(grid_size):
                    sx = scalar(x)
                    sy = scalar(y)
                    sz = scalar(z)
                    self.nodes.append(Node((sx, sy, sz)))

    def drawNodes(self, screen):
        for node in self.nodes:
            node.draw(screen)