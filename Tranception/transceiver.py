from enum import Enum
from debug  import debug

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
    
    def report(self):
        debug(3, f" > (( Transceiver {self.idx} - {self.polarity})):")
        debug(3, f" \t\tReflector A: {self.a.idx} \n\t\tReflector B: {self.b.idx}")
              
        debug(3, f"\t\tPolarity: {self.polarity} \n\t\tInduction: {self.induction} \n\t\tInterference: {self.interference}")

    def __str__(self):
        return str(f" > (( Transceiver {self.idx} )): \n\t\tPolarity: {self.polarity} \n\t\tInduction: {self.induction} \n\t\tInterference: {self.interference}")
    
    def __repr__(self):
        return str(self)