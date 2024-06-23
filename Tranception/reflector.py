describe = lambda idx, cartesian: f"Index: {idx} Cartesian: {cartesian}"

# A Reflection signifies a connection between two reflectors
class Reflection:
    def __init__(self, idx, a, b, similance = True): 
        # The ID should always be equivalent to A's ID, but may be unique in higher order dimensions, and will break offsets
        # when wrapping around the grid via toroidal connections
        self.idx = idx
        self.a = a
        self.b = b
        self.polarity = similance   # This determines if the reflection is similar or opposite
        self.induction = 0.0        # This determines positive or negative flow
        self.interference = 0.0     # This determines constructive or destructive flow
    
    def __str__(self):
        return str(f"\tReflection {self.idx}:: \n\t\t\tSimilance: {self.similance} \n\t\t\tInduction: {self.induction} \n\t\t\tInterference: {self.interference}")
    
    def __repr__(self):
        return str(self)

class Reflector:
    def __init__(self, idx, cartesian):
        self.idx = idx
        self.x, self.y, self.z = cartesian
        self.cartesian = lambda: (self.x, self.y, self.z)
        self.reflections = set()  # These are the reflections that are connected to this reflector

    def __str__(self):
        reflector = str(f"Reflector {describe(self.idx, self.cartesian())}")

        for reflection in self.reflections:
            reflector += f"\n\tNeighbor: \n\t{reflection}"
            similance = "neighbor" if reflection.similance else "opposition"
            reflector += f"\n\t\tSimilance: {similance}"
        
        return reflector
    
    def __repr__(self):
        return str(self)
    
    # This function could be modified to connect new reflectors and determine their influence
    def isOrthogonal(self, neighbor_cartesians):
        neighbor_x, neighbor_y, neighbor_z = neighbor_cartesians

        # If X,Y || X,Z || Y,Z are the same, then we have a neighbor
        match_box = 0
        match_box += 1 if self.x == neighbor_x else 0
        match_box += 1 if self.y == neighbor_y else 0
        match_box += 1 if self.z == neighbor_z else 0

        return match_box >= 2 



