
from node import Node
import asyncio

class Tranception:
    def __init__(self):
        self.model = None # We don't know what this looks like 
        self.tokenizer = None # DONT: This is laughable (at least here)
        self.device = None # TODO: Integrate with Nova
        # Ignore these, they are conceptual
        self.reflectors = [Node(i) for i in range(4)]
        self.reflect()

    def reflect(self):
        [self.reflectors[i].transceivers.add(self.reflectors[(i + j) % 4]) \
            for i in range(4) \
                for j in range(1, 4)]
    

    async def induce(self):
        print("Evoker Inducing Tranception")
        print("")
        print(" - creating reflections")
        reflections = [asyncio.create_task(self.reflectors[0].incept())]
        reflections += [asyncio.create_task(self.reflectors[0].snd(self.reflectors[i])) for i in range(1, 4)]
        print(" - reflections created. awaiting...")
        print("")
        return await asyncio.gather(*reflections)