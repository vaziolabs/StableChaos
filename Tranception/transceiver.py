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
        print(f"\t\t\t - Transceiver {self.identify()} initialized")

    # Takes a tuple of id's and returns True if the reflector set contains the id's
    def contains(self, reflector_set):
        a_id, b_id = reflector_set
        return self.a.idx == a_id and self.b.idx == b_id or self.a.idx == b_id and self.b.idx == a_id

    def __str__(self):
        return str(f" > (( Transceiver {self.identify()} \t)): \n\t\tInduction: {self.induction}")
    
    def __repr__(self):
        return str(self)

    def identify(self):
        return f"{self.polarity}_{self.idx}"

    def fullReport(self):
        print(f" > (( {self.identify()} )) ::\n" \
                f"\t[{self.a.idx} - {self.a.origin()}" \
                f"\t {self.b.idx}{self.b.origin()}]"\
                f"\tA:\n{self.a.report()}" \
                f"\tB:\n{self.b.report()}" \
                f"\tInduction: {self.induction}")

    async def report(self):
        debug(3, f" > (( Transceiver \t{self.identify()}  \t)) :: [{self.a.origin()}-{self.b.origin()}] \t:  \t{self.induction}")

    async def reflect(self):
        self.induction = self.divergence(self.interference())

    def phaseDifference(self):
        return ((self.a.theta - self.b.theta)  + 360) % 360

    def interference(self):
        # If the phase difference is between 0 and 90, or 270 and 360, we are in phase
        if 90 <= self.phaseDifference() < 270:
            return self.a.theta - self.b.theta
        
        # If the phase difference is between 90 and 180, or 180 and 270, we are out of phase
        return self.a.theta + self.b.theta

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

