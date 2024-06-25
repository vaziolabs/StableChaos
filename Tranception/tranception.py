
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
        self.adjacencies = 0
        self.orthogonals = 0
        self.polars = 0
        self.self_reflections = 0
        self.uncaught = 0
        self.realize() 

    # Returns previous count for indexing purposes, and increments the count
    def count(self, reflection_type):
        previous = 0

        if reflection_type == Polarity.Adjacent:
            previous = self.adjacencies
            self.adjacencies += 1
        if reflection_type == Polarity.Orthogonal:
            previous = self.orthogonals
            self.orthogonals += 1
        if reflection_type == Polarity.Polar:
            previous = self.polars
            self.polars += 1
        if reflection_type == Polarity.Self:
            previous = self.self_reflections
            self.self_reflections += 1
        if reflection_type is None:
            previous = self.uncaught
            self.uncaught += 1

        return previous

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
                                    self_reflection = Transceiver(self.self_reflections, reflector, reflector, Polarity.Self)
                                    reflector.addReflection(self_reflection)
                                    self.reflections.add(self_reflection)
                                    self.self_reflections += 1
                                    continue

                                # We assume that the neighbor does not exist
                                neighbor = None
                                reflection = None

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

                                for reflecting in self.reflections:
                                    if reflecting.contains((reflector.idx, neighbor.idx)):
                                        reflection = reflecting
                                        break

                                debug(4 , f"\t\t\tReflection Exists: {reflection is not None}")
                                # If we have not seen the reflection, we add it
                                if reflection is None:
                                    debug(4 ,"\t\t\tAdding Transceiver Connection:")
                                    reflection_type = reflector.reflectionType(neighbor.origin()) # This is here for logging purposes
                                    
                                    reflection = Transceiver(self.count(reflection_type), reflector, neighbor, reflection_type) # This is where we need to also add a new reflection

                                    self.reflections.add(reflection)
                                    reflector.addReflection(reflection)
                                    neighbor.addReflection(reflection)
        self.report()

    def report(self):
        debug(4, f"Realized Grid of {len(self.reflectors)} Reflectors")    
        # for reflector in self.reflectors:
        #     print(reflector)
        
        polar_reclections = len([reflection for reflection in self.reflections if reflection.polarity == Polarity.Polar])
        adjacent_reclections = len([reflection for reflection in self.reflections if reflection.polarity == Polarity.Adjacent])
        orthogonal_reclections = len([reflection for reflection in self.reflections if reflection.polarity == Polarity.Orthogonal])
        self_reflections = len([reflection for reflection in self.reflections if reflection.polarity == Polarity.Self])
        uncaught_reflections = len([reflection for reflection in self.reflections if reflection.polarity is None])
        debug(4, f"\nRealized Network of {len(self.reflections)} Transceiver Reflections")
        debug(4, f"\tOrthogonal: {orthogonal_reclections} / {self.orthogonals}")
        debug(4, f"\tAdjacent: {adjacent_reclections} / {self.adjacencies}")
        debug(4, f"\tPolar: {polar_reclections} / {self.polars}")
        debug(4, f"\tSelf: {self_reflections} / {self.self_reflections}")
        debug(4, f"\tUncaught: {uncaught_reflections} / {self.uncaught}")
        # for reflection in self.reflections:
        #     reflection.fullReport() 


    async def actualize(self):
        # This is where we need to see what happens when we start the tranception process
        # Resonate, Reflect, Transceive, Resolve, Observe
        return

        resonators = [reflector.resonate() for reflector in self.reflectors]
        reflections = [reflection.reflect() for reflection in self.reflections]
        reports = [reflection.report() for reflection in self.reflections]

        return await asyncio.gather(*resonators, *reflections, *reports)
        

    def observe(self):
        pass