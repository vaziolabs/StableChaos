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
    
    def report(self):
        debug(3, f" > (( Transceiver {self.idx} - {self.polarity})):")
        debug(3, f" \t\tReflector A: {self.a.idx} \n\t\tReflector B: {self.b.idx}")
              
        debug(3, f"\t\tPolarity: {self.polarity} \n\t\tInduction: {self.induction} \n\t\tInterference: {self.interference}")

    def reflect(self):
        self.induction = self.divergence(self.interference())

    def phaseDifference(self):
        return ((self.a.theta - self.b.theta)  + 360) % 360

    def interference(self):
        # If the phase difference is between 0 and 90, or 270 and 360, we are in phase
        if 90 <= self.phaseDifference() < 270:
            return self.a - self.b
        
        # If the phase difference is between 90 and 180, or 180 and 270, we are out of phase
        return self.a + self.b

    def divergence(self, interference):
        if self.polarity == Polarity.Self:
            return 0.0
    
        if self.polarity == Polarity.Orthogonal:
            theta_a = self.a.theta
            theta_b = self.b.theta
            if theta_a < theta_b:
                return interference
            if theta_a > theta_b:
                return -1.0 * interference
        
        if self.polarity == Polarity.Adjacent:
            return interference
        
        if self.polarity == Polarity.Polar:
            return -1.0 * interference

    def __str__(self):
        return str(f" > (( Transceiver {self.idx} )): \n\t\tPolarity: {self.polarity} \n\t\tInduction: {self.induction} \n\t\tInterference: {self.interference}")
    
    def __repr__(self):
        return str(self)