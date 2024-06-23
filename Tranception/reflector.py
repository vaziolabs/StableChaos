from enum import Enum


# A Reflection signifies a connection between two reflectors
class Reflection:
    def __init__(self, idx, neighbor):
        self.idx = idx
        self.is_neighbor = neighbor
        self.induction = 0.0
        self.interference = 0.0
    
    def __str__(self):
        return str("Reflection", self.idx)

class Reflector:
    def __init__(self, idx):
        self.idx = idx
        self.reflections = set()  # These are direct neighbors we tend to follow

    def __str__(self):
        reflector = str("Reflector {self.idx}")

        for reflection in self.reflections:
            reflector += f"\n\tNeighbor: {reflection}"
            similance = "neighbor" if reflection.is_neighbor else "opposition"
            reflector += f"\n\tSimilance: {similance}"
        
        return reflector

normalize_idx = lambda idx, width: (idx % width, idx // width)

# If the node, and the neighbor are in the same row, they are neighbors
# or, if they are in the same column, they are neighbors, otherwise they oppose
def isNeighbor(node_idx, neighbor_idx, width):
    node_col_id, node_row_id = normalize_idx(node_idx, width)
    neighbor_col_id, neighbor_row_id = normalize_idx(neighbor_idx, width)
        
    if node_col_id == neighbor_col_id or node_row_id == neighbor_row_id:
        return True
    return False
    
# TODO: Implement configuration models where we only look right or up, 
#       Or we 'square' the grid into a 2D array, into bi-directional connections
#       or we can cube the grid into a 3D array, into n-dimensional connections
#       or we can weave it like a mesh, into fully interconnected nodes

class Dimensionality(Enum):
    Cellular = 1,
    Planar = 2,
    Cubic = 3,

if __name__ == "__main__":
    dimensions = Dimensionality.Planar
    grid_size = 3
    # This constructs a set of reflectors and reflections for a 2x2 grid, without respect to X and Y
    reflectors = [Reflector(i) for i in range(grid_size * grid_size)]
    reflections = [] # This is where we determine dimensionality

    index_counter = 0
    while index_counter < len(reflectors):
        reflector = reflectors[index_counter]

        if index_counter + 1 > grid_size:

            continue
    


    for reflector in reflectors:
        print(reflector)
        


