from enum import Enum

x = lambda idx, grid_size: idx % grid_size
y = lambda idx, grid_size: idx % (grid_size * grid_size) // grid_size
z = lambda idx, grid_size: idx // (grid_size * grid_size)
unwrap = lambda idx, grid_size: (x(idx, grid_size), y(idx, grid_size), z(idx, grid_size))

def describe(index, grid_size):
    x, y, z = unwrap(index, grid_size)
    return f"Index: {index} Cartesian: ({x}, {y}, {z})"

# A Reflection signifies a connection between two reflectors
class Reflection:
    def __init__(self, idx, a, b, similance): 
        # The ID should always be equivalent to A's ID, but may be unique in higher order dimensions, and will break offsets
        # when wrapping around the grid via toroidal connections
        self.idx = idx
        self.a = a
        self.b = b
        self.similance = similance   # This determines if the reflection is similar or opposite
        self.induction = 0.0        # This determines positive or negative flow
        self.interference = 0.0     # This determines constructive or destructive flow
    
    def __str__(self):
        return str("Reflection", describe(self.idx), "Similance: ", self.similance, "Induction: ", self.induction, "Interference: ", self.interference)
    
    def __repr__(self):
        return str(self)

class Reflector:
    def __init__(self, idx):
        self.idx = idx
        self.reflections = set()  # These are the reflections that are connected to the reflector
        self.normalize = lambda idx, width: (idx % width, idx // width)

    def addReflection(self, reflection,):
        self.reflections.add(reflection)

    def __str__(self):
        reflector = str("Reflector ", describe(self.idx))

        for reflection in self.reflections:
            reflector += f"\n\tNeighbor: {reflection}"
            similance = "neighbor" if reflection.is_neighbor else "opposition"
            reflector += f"\n\tSimilance: {similance}"
        
        return reflector
    
    def __repr__(self):
        return str(self)
    
    # This function could be modified to connect new reflectors and determine their influence
    def isNeighbor(idx, neighbor_idx, width):
        # If X,Y || X,Z || Y,Z are the same, then we have a neighbor
        self_x, self_y, self_z = unwrap(idx, width)
        neighbor_x, neighbor_y, neighbor_z = unwrap(neighbor_idx, width)
        
        match_box = 0
        match_box += 1 if self_x == neighbor_x else 0
        match_box += 1 if self_y == neighbor_y else 0
        match_box += 1 if self_z == neighbor_z else 0

        return match_box >= 2 


# TODO: Implement this for varying configurations of the grid
class Dimensionality(Enum):
    Sparse = 1,         # This is does not look angular, but is interconnected e.g. Left, Right, Up, Down, Forward, Backward (not-combinatorially connected)
    Sparse_Torus = 2,   # This is the 2D network that wraps around itself, nd - circular
    Cubic = 4,          # This is an interconnected network that is 3D in nature
    Cubic_Toroidal = 5, # This is the 3D network that wraps around itself in all dimensions, nd - spherical
    Hyper = 6           # This is a configuration of Every Node connecting to one another

    __str__ = lambda self: self.name
        


