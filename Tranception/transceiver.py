from enum import Enum

class Polarity(Enum):
    Self = 0
    Orthogonal = 1
    Adjacent = 2
    Polar = 3
    __str__ = lambda self: self.name

# A Reflection signifies a connection between two reflectors
class Transceiver: 
    def __init__(self, idx, a, b, similance): 
        # The ID should always be equivalent to A's ID, but may be unique in higher order dimensions, and will break offsets
        # when wrapping around the grid via toroidal connections
        self.idx = idx
        self.a = a
        self.b = b
        self.polarity = similance   # This determines if the reflection is similar or opposite
        self.induction = 0.0        # This determines positive or negative flow
        self.interference = 0.0     # This determines constructive or destructive flow
    
    def __str__(self):
        return str(f"\tReflection {self.idx}:: \n\t\t\tPolarity: {self.polarity} \n\t\t\tInduction: {self.induction} \n\t\t\tInterference: {self.interference}")
    
    def __repr__(self):
        return str(self)