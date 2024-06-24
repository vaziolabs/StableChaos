
from reflector import Reflector
from transceiver import Transceiver
import asyncio

sample_frequency = 44100

# This is the parent class that enacts the tranception process
#  which is synchronous and asynchronous in nature
class Tranception:
    def __init__(self, grid_size, dimensional, configuration):
        self.dimensionality = dimensional   # TODO: Implement these dimensions
        self.configuration = configuration  # TODO: Implement these configurations
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
    def realize(self):
        for z in range(self.grid_size):
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    grid_index = z * self.grid_size * self.grid_size + y * self.grid_size + x
                    print(" > Realizing Reflector: ", grid_index)
                    # This creates a "node" in our grid
                    reflector = Reflector(grid_index, (x, y, z))
                    self.reflections.add(reflector)

                    # We want to iterate within our bounds
                    min_x = max(0, x - 1)
                    min_y = max(0, y - 1)
                    min_z = max(0, z - 1)
                    max_x = min(self.grid_size - 1, x + 1)
                    max_y = min(self.grid_size - 1, y + 1)
                    max_z = min(self.grid_size - 1, z + 1)
                    print("\tGrid Index: ", grid_index)
                    print("\tGrid Cartesian: ", reflector.cartesian())
                    print(f'\t min: ({min_x}, {min_y}, {min_z}), max: ({max_x}, {max_y}, {max_z})')

                    # This is where we interconnect the reflectors and their reflections
                    for neighbor_z in range(min_z, max_z + 1):
                        for neighbor_y in range(min_y, max_y + 1):
                            for neighbor_x in range(min_x, max_x + 1):
                                neighbor_idx = neighbor_z * self.grid_size * self.grid_size + neighbor_y * self.grid_size + neighbor_x
                                print("\t\tVisiting Neighbor: ", neighbor_idx)
                                print("\t\tNeighbor Cartesian: ", (neighbor_x, neighbor_y, neighbor_z))

                                # If we are at outselve, we add a self reflection
                                if neighbor_idx == grid_index:
                                    print("\t\t\tAdding Self Reflection")
                                    self_reflection = Transceiver(len(self.reflections), reflector, reflector, reflector.reflectionType((neighbor_x, neighbor_y, neighbor_z)))
                                    reflector.addReflection(self_reflection)
                                    continue

                                # We assume that the neighbor does not exist
                                neighbor = None

                                # Check if we have seen the neighbor before
                                for reflector in self.reflectors:
                                    if reflector.idx == neighbor_idx:
                                        neighbor = reflector
                                        break
                                
                                print("\t\t\tNeighbor", neighbor_idx, "Exists: ", neighbor is not None)
                                # If we have not seen the neighbor, we add it and it's reflection
                                if neighbor is None:
                                    # while determining if it has similance or opposition
                                    neighbor = Reflector(neighbor_idx, (neighbor_x, neighbor_y, neighbor_z))
                                    self.reflectors.add(neighbor)
                                    print("\t\t\tAdding Neighbor Reflection:", reflector.reflectionType(neighbor.cartesian()))
                                    # This is where we need to also add a new reflection
                                    reflection = Transceiver(len(self.reflections), reflector, neighbor, reflector.reflectionType(neighbor.cartesian()))

                                    self.reflections.add(reflection)
                                    reflector.addReflection(reflection)
                                    neighbor.addReflection(reflection)
    
        for reflector in self.reflectors:
            print(reflector)


    async def actualize(self):
        return

    def observe(self):
        pass