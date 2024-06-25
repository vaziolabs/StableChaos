
from Tranception import Orientation, Dimensionality
from Tranception.reflector import Reflector
from Tranception.coupling import Coupling
from Tranception.debug import debug
import asyncio

sample_frequency = 44100

# This is the parent class that enacts the tranception process
#  which is synchronous and asynchronous in nature
class Tranceptor:
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

        if reflection_type == Orientation.Adjacent:
            previous = self.adjacencies
            self.adjacencies += 1
        if reflection_type == Orientation.Orthogonal:
            previous = self.orthogonals
            self.orthogonals += 1
        if reflection_type == Orientation.Polar:
            previous = self.polars
            self.polars += 1
        if reflection_type == Orientation.Self:
            previous = self.self_reflections
            self.self_reflections += 1
        if reflection_type is None:
            previous = self.uncaught
            self.uncaught += 1

        return previous

    # This is essentially our 'init' function for wiring up the mirrors
    # This is where we will plug in some configuration for dimensions and grid size, as well
    # as configurations for the interconnectedness of the reflectors

    # TODO: Implement the ability to add a filter AND/OR Convolutions for the reflections
    def realize(self):
        if self.dimensionality == Dimensionality.Cubic:
            self.construct3DMesh()
        elif self.dimensionality == Dimensionality.Planar:
            self.constructPlanarMesh()
        elif self.dimensionality == Dimensionality.Linear:
            self.constructLinearMesh()
        
        self.report()

    def report(self):
        debug(4, f"Realized Grid of {len(self.reflectors)} Reflectors")    
        # for reflector in self.reflectors:
        #     print(reflector)
        
        polar_reclections = len([reflection for reflection in self.reflections if reflection.polarity == Orientation.Polar])
        adjacent_reclections = len([reflection for reflection in self.reflections if reflection.polarity == Orientation.Adjacent])
        orthogonal_reclections = len([reflection for reflection in self.reflections if reflection.polarity == Orientation.Orthogonal])
        self_reflections = len([reflection for reflection in self.reflections if reflection.polarity == Orientation.Self])
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

    # DEPRECATED
    ## Can we do this for the entire network at once?
    async def reflect(self): #punnyhashtags
        return await asyncio.gather(*[self.reflectors[i].snd(self.reflectors[(i + j) % self.grid_size]) \
            for i in range(self.size) \
                for j in range(1, self.size)])

    # DEPRECATED
    # We are using the verbiage 'reflections' here to express the way that all of the 
    # nodes are responding to a single timesteps 'inception' of a signal (440 in this case)
    async def induce(self):
        print("Evoker Inducing Tranception")
        print("")
        print(" - creating reflections")
        reflections = [reflector.incept(sample_frequency) for reflector in self.reflectors]
        reflections += [reflection.reflect() for reflection in self.reflections]
        print(" - reflections created. awaiting...")
        print("") 
        return await asyncio.gather(*reflections)
    
    # Constructor-ish function for the reflectors
    def constructLinearMesh(self):
            for x in range(self.grid_size):
                debug(4 ,f" > Realizing Reflector: {x}")
                # This creates a "node" in our grid
                reflector = Reflector(x, (x, 0, 0))
                self.reflectors.add(reflector)

                # We want to iterate within our bounds
                min_x = max(0, x - 1)
                max_x = min(self.grid_size - 1, x + 1)
                debug(4 ,f"\tGrid Index: {x}")
                debug(4 ,f"\t\tGrid Cartesian: {reflector.origin()}")
                debug(4 ,f'\t\t min: ({min_x}), max: ({max_x})')

                # This is where we interconnect the reflectors and their reflections
                for neighbor_x in range(min_x, max_x + 1):
                    neighbor_idx = neighbor_x
                    debug(4 , f"\t\tVisiting Neighbor: {neighbor_idx}")
                    debug(4 , f"\t\t\tNeighbor Cartesian: {(neighbor_x, 0, 0)}")

                    # If we are at outselve, we add a self reflection
                    if neighbor_idx == x:
                        debug(4 ,"\t\t\tAdding Self Reflection")
                        self_reflection = Coupling(self.self_reflections, reflector, reflector, Orientation.Self)
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
                        neighbor = Reflector(neighbor_idx, (neighbor_x, 0, 0))
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
                        
                        reflection = Coupling(self.count(reflection_type), reflector, neighbor, reflection_type) # This is where we need to also add a new reflection

                        self.reflections.add(reflection)
                        reflector.addReflection(reflection)
                        neighbor.addReflection(reflection)

    # Constructor-ish function for the reflectors
    def constructPlanarMesh(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                grid_index = y * self.grid_size + x
                debug(4 ,f" > Realizing Reflector: {grid_index}")
                # This creates a "node" in our grid
                reflector = Reflector(grid_index, (x, y, 0))
                self.reflectors.add(reflector)

                # We want to iterate within our bounds
                min_x = max(0, x - 1)
                min_y = max(0, y - 1)
                max_x = min(self.grid_size - 1, x + 1)
                max_y = min(self.grid_size - 1, y + 1)
                debug(4 ,f"\tGrid Index: {grid_index}")
                debug(4 ,f"\t\tGrid Cartesian: {reflector.origin()}")
                debug(4 ,f'\t\t min: ({min_x}, {min_y}), max: ({max_x}, {max_y})')

                # This is where we interconnect the reflectors and their reflections
                for neighbor_y in range(min_y, max_y + 1):
                    for neighbor_x in range(min_x, max_x + 1):
                        neighbor_idx = neighbor_y * self.grid_size + neighbor_x
                        debug(4 , f"\t\tVisiting Neighbor: {neighbor_idx}")
                        debug(4 , f"\t\t\tNeighbor Cartesian: {(neighbor_x, neighbor_y, 0)}")

                        # If we are at outselve, we add a self reflection
                        if neighbor_idx == grid_index:
                            debug(4 ,"\t\t\tAdding Self Reflection")
                            self_reflection = Coupling(self.self_reflections, reflector, reflector, Orientation.Self)
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
                            neighbor = Reflector(neighbor_idx, (neighbor_x, neighbor_y, 0))
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
                            
                            reflection = Coupling(self.count(reflection_type), reflector, neighbor, reflection_type) # This is where we need to also add a new reflection

                            self.reflections.add(reflection)
                            reflector.addReflection(reflection)
                            neighbor.addReflection(reflection)


    # Constructor-ish function for the reflectors
    def construct3DMesh(self):
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
                                    self_reflection = Coupling(self.self_reflections, reflector, reflector, Orientation.Self)
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
                                    
                                    reflection = Coupling(self.count(reflection_type), reflector, neighbor, reflection_type) # This is where we need to also add a new reflection

                                    self.reflections.add(reflection)
                                    reflector.addReflection(reflection)
                                    neighbor.addReflection(reflection)