import asyncio
from tc_engine import TCEngine

# TODO: 
#       Graph single node - single phase.. 
#       Scale to multiple nodes simultaneously
#       Color Code the nodes via the Engine
#       Build Path and Particle System
#       Add Gravity/Induction Cross Analysis
#       Abstract the Transceiver functions away from the Node, and into Transmission
#       Integrate with Nova and risc-v via SKIFT


def main():
    print(" ~~~~  Tranception dude!  ~~~~~")

    engine = TCEngine((1600, 1200))
    engine.run(engine.activate)

if __name__ == '__main__':
    main()