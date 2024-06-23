import asyncio
import sys
from tranception_new import Tranception
sys.path.append('../')
from engine import Engine, Color
from enum import Enum

# TODO: Abstract a concurent Library for the Engine seperate from the Sampling of the Tranception process.
#       The game engine is meant to observe at 60hz, while the tranception process is meant to 'sample' at 44.1khz 
# TODO: Chunk 'prefix' our waveforms to be able to stretch, compress and cache the waveforms
# TODO: Implement Waveform Analysis and Synthesis as well as color coding

class Configuration(Enum):
    Sparse = 0,         # This is a configuration where the nodes are not connected to one another, by default
    Othogonal = 1,      # This is a configuration where the nodes are connected to their neighbors but not opposers
    Adjacency = 2,      # This is a configuration where the nodes are connected to their neighbors and opposers
    Toroidal = 3,       # This is a configuration where the nodes are connected to their neighbors and opposers, and wrap around the grid
    Hyper = 4           # This is a configuration where the nodes are connected to every other node 
    __str__ = lambda self: self.name

class Dimensionality(Enum):
    Planar = 0,         # This is a 2D configuration
    Cubic = 1,          # This is a 3D configuration
    Tetrahedral = 2,    # This is a higher order configuration that can only be configured as orthogonal or adjacency (toroidal and hyper are adjacents)
    __str__ = lambda self: self.name


# This is a wrapper function that interfaces with the game engine through the Engine class
class TCEngine(Engine):
    def __init__(self, screen_size, grid_size, dimensionality, configuration):
        super().__init__(screen_size, [])
        self.instance = Tranception(grid_size, configuration, dimensionality) # We could abstract away TC_Engine and Tranception into a single class eventually

    # This allows for concurrent execution of the tranception processes.
    # This is called every frame of our game loop (60 times per second) ((not 44.1khz!!)) <- This is an entirely different problem
    def activate(self,):
        asyncio.run(self.instance.actualize())

