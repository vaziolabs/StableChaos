
from node import Node
import asyncio

sample_frequency = 44100

# This is the parent class that enacts the tranception process
#  which is synchronous and asynchronous in nature
class Tranception:
    def __init__(self, size):
        self.size = size
        # self.model = None # We don't know what this looks like 
        # self.tokenizer = None # DONT: This is laughable (at least here)
        # self.device = None # TODO: Integrate with Nova
        # Ignore these, they are conceptual
        self.reflectors = [Node(i) for i in range(size)]
        self.realize() 

    ## This function simply 'zips' all of our transceivers connections together through the nodes
    def realize(self):
        [self.reflectors[i].connections.add(self.reflectors[(i + j) % self.size]) \
            for i in range(self.size) \
                for j in range(1, self.size)]

    ## Can we do this for the entire network at once?
    async def reflect(self): #punnyhashtags
        return await asyncio.gather(*[self.reflectors[i].snd(self.reflectors[(i + j) % self.size]) \
            for i in range(self.size) \
                for j in range(1, self.size)])

    # We are using the verbiage 'reflections' here to express the way that all of the 
    # nodes are responding to a single timesteps 'inception' of a signal (440 in this case)
    async def induce(self):
        print("Evoker Inducing Tranception")
        print("")
        print(" - creating reflections")
        reflections = [asyncio.create_task(self.reflectors[0].incept())]
        reflections += [asyncio.create_task(self.reflectors[0].snd(self.reflectors[i])) for i in range(1, self.size)]
        print(" - reflections created. awaiting...")
        print("") 
        return await asyncio.gather(*reflections)