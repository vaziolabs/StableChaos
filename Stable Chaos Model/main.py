# Here we are simply displaying 4 nodes that each have a XYZW value, which we represent using RGBW values,
# with W being the brightness of the LED. We are using the Pygame library to display the nodes on the screen.
from sc_engine import SCEngine 
from node import Node
from position import Position
from engine import Color

# Set the screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200

# Instantiate our nodes
nodes = [Node(Position(i, SCREEN_WIDTH, SCREEN_HEIGHT), Color.WHITE_FILL) for i in range(4)]

# Initialize our Engine
engine = SCEngine((SCREEN_WIDTH, SCREEN_HEIGHT), nodes)

if __name__ == "__main__":
    engine.run(engine.cycle)