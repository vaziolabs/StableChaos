from enum import Enum   

class Settings(Enum):
    SCREEN_SIZE = 1200
    GRID_SIZE = 10
    HALF_SCREEN = SCREEN_SIZE // 2
    NODE_SPACING = HALF_SCREEN // (GRID_SIZE - 1)
    GRID_OFFSET = HALF_SCREEN // 2
    NODE_SIZE = 10