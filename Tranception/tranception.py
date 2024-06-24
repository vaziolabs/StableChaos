
from reflector import Reflector
from transceiver import Polarity, Transceiver
from debug import debug
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
                    debug(4 ,f" > Realizing Reflector: {grid_index}")
                    # This creates a "node" in our grid
                    reflector = Reflector(grid_index, (x, y, z))
                    self.reflectors.add(reflector)

                    # We want to iterate within our bounds
                    min_x = max(0, x - 1)
                    min_y = max(0, y - 1)
                    min_z = max(0, z - 1)
                    max_x = min(self.grid_size - 1, x + 1)
                    max_y = min(self.grid_size - 1, y + 1)
                    max_z = min(self.grid_size - 1, z + 1)
                    debug(4 ,f"\tGrid Index: {grid_index}")
                    debug(4 ,f"\t\tGrid Cartesian: {reflector.origin()}")
                    debug(4 ,f'\t\t min: ({min_x}, {min_y}, {min_z}), max: ({max_x}, {max_y}, {max_z})')

                    # This is where we interconnect the reflectors and their reflections
                    for neighbor_z in range(min_z, max_z + 1):
                        for neighbor_y in range(min_y, max_y + 1):
                            for neighbor_x in range(min_x, max_x + 1):
                                neighbor_idx = neighbor_z * self.grid_size * self.grid_size + neighbor_y * self.grid_size + neighbor_x
                                debug(4 , f"\t\tVisiting Neighbor: {neighbor_idx}")
                                debug(4 , f"\t\t\tNeighbor Cartesian: {(neighbor_x, neighbor_y, neighbor_z)}")

                                # If we are at outselve, we add a self reflection
                                if neighbor_idx == grid_index:
                                    debug(4 ,"\t\t\tAdding Self Reflection")
                                    self_reflection = Transceiver(len(self.reflections), reflector, reflector, Polarity.Self)
                                    reflector.addReflection(self_reflection)
                                    self.reflections.add(self_reflection)
                                    continue

                                # We assume that the neighbor does not exist
                                neighbor = None

                                # Check if we have seen the neighbor before
                                for reflected in self.reflectors:
                                    if reflected.idx == neighbor_idx:
                                        neighbor = reflected
                                        break
                                
                                debug(4 ,f"\t\t\tNeighbor {neighbor_idx} Exists: {neighbor is not None}")
                                # If we have not seen the neighbor, we add it and it's reflection
                                # while determining if it has reflection type
                                if neighbor is None:
                                    debug(4 , f"\t\t\t\tAdding Reflector {neighbor_idx}")
                                    neighbor = Reflector(neighbor_idx, (neighbor_x, neighbor_y, neighbor_z))
                                    self.reflectors.add(neighbor)

                                    debug(4 ,"\t\t\tAdding Neighbor Reflection:")
                                    reflection_type = reflector.reflectionType(neighbor.origin()) # This is here for logging purposes
                                    reflection = Transceiver(len(self.reflections), reflector, neighbor, reflection_type) # This is where we need to also add a new reflection

                                    self.reflections.add(reflection)
                                    reflector.addReflection(reflection)
                                    neighbor.addReflection(reflection)

        print("Realized Grid of Reflectors")    
        for reflector in self.reflectors:
            print(reflector)
        
        print("\nRealized Network of Reflections\n")
        for reflection in self.reflections:
            reflection.report()


    async def actualize(self):
        return

    def observe(self):
        pass