from enum import Enum

class Orientation(Enum):
    Self = 0
    Orthogonal = 1
    Adjacent = 2
    Polar = 3
    OutOfRange = 4
    __str__ = lambda self: self.name

class Configuration(Enum):
    Sparse = 0,         # This is a configuration where the nodes are not connected to one another, by default
    Othogonal = 1,      # This only connects to nodes that are in the same x, y, or z plane
    Adjacency = 2,      # This is a configuration where the nodes are a combination of X, Y, and Z planes
    Polar = 3,          # This is when it is +/- 1 in all directions
    Hyper = 4           # This is a configuration where the nodes are connected to every other node 
    __str__ = lambda self: self.name

class Dimensionality(Enum):
    Linear = 0,         # This is a 1D configuration
    Planar = 1,         # This is a 2D configuration
    Cubic = 2,          # This is a 3D configuration
    Toroidal = 3,       # This is a Simply Wrapps around the edges
    __str__ = lambda self: self.name

class Directionality(Enum):
    Forward = 0,        # This allows flow to move to the right
    Backward = 1,       # This allows flow to move to the left
    Radio = 2,          # This allows flow to move in all directions
    __str__ = lambda self: self.name