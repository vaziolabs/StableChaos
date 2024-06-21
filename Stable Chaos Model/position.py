# We are subdividing our screen into 4 positions, from the top left
POSITIONS = [
    (1, 2), 
    (2, 1),
    (3, 2),
    (2, 3)
]


class Position:
    def __init__(self, position, screen_width, screen_height):
        self.idx = position
        self.x = screen_width // 4 * POSITIONS[position][0]
        self.y = screen_height // 4 * POSITIONS[position][1]
        