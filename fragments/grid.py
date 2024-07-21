from .node import Node
from .settings import Settings

class Grid:
    def __init__(self):
        self.nodes = []
        for x in range(Settings.GRID_SIZE.value):
            for y in range(Settings.GRID_SIZE.value):
                for z in range(Settings.GRID_SIZE.value):
                    self.nodes.append(Node((x, y, z)))

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)