import asyncio
from tc_engine import TCEngine
from reflector import Dimensionality

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

    grid_size = 3
    dimensionality = Dimensionality.Cubic
    

    engine = TCEngine((1600, 1200), grid_size, dimensionality)
    engine.run(engine.activate)

if __name__ == '__main__':
    main()