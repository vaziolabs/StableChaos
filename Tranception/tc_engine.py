import asyncio
import sys
from tranception_new import Tranception
sys.path.append('../')
from engine import Engine, Color

# TODO: Abstract a concurent Library for the Engine seperate from the Sampling of the Tranception process.
#       The game engine is meant to observe at 60hz, while the tranception process is meant to 'sample' at 44.1khz 
# TODO: Chunk 'prefix' our waveforms to be able to stretch, compress and cache the waveforms
# TODO: Implement Waveform Analysis and Synthesis as well as color coding

# This is a wrapper function that interfaces with the game engine through the Engine class
class TCEngine(Engine):
    def __init__(self, screen_size, grid_size, dimensions):
        super().__init__(screen_size, [])
        self.instance = Tranception(grid_size, dimensions) # Based on Grid Size

    # This allows for concurrent execution of the tranception processes.
    # This is called every frame of our game loop (60 times per second) ((not 44.1khz!!)) <- This is an entirely different problem
    def activate(self,):
        asyncio.run(self.instance.realize())

