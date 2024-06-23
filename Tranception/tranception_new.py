
from reflector import Reflector, Reflection
import asyncio

sample_frequency = 44100



# This is the parent class that enacts the tranception process
#  which is synchronous and asynchronous in nature
class Tranception:
    def __init__(self, grid_size, dimensions):
        self.configuration = dimensions
        self.grid_size = grid_size
        self.reflectors = set()
        self.reflections = set()
        self.realize() 

    # This is essentially our 'init' function for wiring up the mirrors
    # This is where we will plug in some configuration for dimensions and grid size, as well
    # as configurations for the interconnectedness of the reflectors

    # TODO: Implement a filter AND/OR Convolutions for the reflections
    # TODO: Implement the config where
        # We connect to the right and down neighbors only 
        # We connect to all neighbors within the bounding box set to the grid size
        # We connect to the neighbors based on 3D coordinates
        # We add toroidal connections to the grid, wrapping around the grid
    async def realize(self):
        for z in range(self.grid_size):
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    grid_index = z * self.grid_size * self.grid_size + y * self.grid_size + x

                    # This creates a "node" in our grid
                    reflector = Reflector(grid_index, (x, y, z))
                    self.reflections.add(reflector)

                    # We want to iterate within our bounds
                    min_x = max(0, x - 1)
                    min_y = max(0, y - 1)
                    min_z = max(0, z - 1)
                    max_x = min(self.grid_size, x + 1)
                    max_y = min(self.grid_size, y + 1)
                    max_z = min(self.grid_size, z + 1)

                    # This is where we interconnect the reflectors and their reflections
                    for neighbor_z in range(min_z, max_z):
                        for neighbor_y in range(min_y, max_y):
                            for neighbor_x in range(min_x, max_x):
                                neighbor_idx = neighbor_z * self.grid_size * self.grid_size + neighbor_y * self.grid_size + neighbor_x

                                # If we are at outselve, we skip
                                if neighbor_idx == grid_index:
                                    continue

                                # We assume that the neighbor does not exist
                                neighbor = None

                                # Check if we have seen the neighbor before
                                for reflector in self.reflectors:
                                    if reflector.idx == neighbor_idx:
                                        neighbor = reflector
                                        break

                                # If we have not seen the neighbor, we add it and it's reflection
                                if neighbor is None:
                                    # while determining if it has similance or opposition
                                    neighbor = Reflector(neighbor_idx, (neighbor_x, neighbor_y, neighbor_z))
                                    self.reflectors.add(neighbor)

                                    # This is where we need to also add a new reflection
                                    reflection = Reflection(len(self.reflections), reflector, neighbor, reflector.isNeighbor(neighbor.cartesian()))

                                    self.reflections.add(reflection)
                                    reflector.reflections.add(reflection)
                                    neighbor.reflections.add(reflection)
                                    


        for reflector in self.reflectors:
            print(reflector)


    def actualize(self):
        pass

    def observe(self):
        pass