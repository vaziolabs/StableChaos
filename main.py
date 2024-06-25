import asyncio
from Tranception import Configuration, Dimensionality
from Tranception.engine import TCEngine

# TODO: 
#       Graph single node - single phase.. 
#       Scale to multiple nodes simultaneously
#       Color Code the nodes via the Engine
#       Build Path and Particle System
#       Add Gravity/Induction Cross Analysis
#       Abstract the Transceiver functions away from the Node, and into Transmission or Reflection
#       Integrate with Nova and risc-v via SKIFT


# TODO: Implement Toroidal and Hyperdimensional configurations, as well as sparse connections
def main():
    print(" ~~~~  Tranception dude!  ~~~~~")
    start_time = asyncio.get_event_loop().time()
    screen_size = (1600, 1200)
    grid_size = 2
    dimensionality = Dimensionality.Planar
    configuration = Configuration.Adjacency

    engine = TCEngine(screen_size, grid_size, configuration, dimensionality)
    print(f" ~~~~  Tranception dude!  ~~~~~\n\t\t\t - took {asyncio.get_event_loop().time() - start_time:.5f} seconds to initialize.")
    engine.run(engine.activate)

if __name__ == '__main__':
    main()