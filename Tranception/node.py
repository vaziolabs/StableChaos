from transceiver import Transceiver

import asyncio

class Node(Transceiver):
    def __init__(self, idx):
        print(" [[ Node", idx, " initialized ]]")
        super().__init__()
        self.idx = idx
        self.connections = set() # Transceivers are the 'nodes' that are connected to the

    def __str__(self) -> str:
        return str(self.idx)
    
    def __repr__(self) -> str:
        return str(self.idx)

    async def rcv(self, transmission): # Do we want to log who we receptioned from?
        print("  -[ Node Received: ", transmission, " ]")
        self.reception = transmission
        awaiting = await self.resonate()
        print(self.idx, " has resonated at ", self.phase, " with a resulting threshold of ", self.threshold)
        return awaiting
    
    ## This Function is purely for testing and simulation purposes to induce the reception of a signal
    async def incept(self, frequency = 440):
        print(" [ Node Incepted: ", self.idx, " ]")
        i = frequency
        while i > 0:
            await self.rcv(frequency)
            print("|> Incepting: ", i)
            print("theta::", self.theta, ", thrsh::", self.threshold, ", recpt::", self.reception)
            i -= 1

    async def snd(self, other):
        print("  -[ Node Sending: ", self.theta, " to ", other.idx, " ]")
        self.reception = (self.theta + other.threshold) / 2.0
        await self.resonate()
        return await other.rcv(self.theta)
    
    ## This function is purely to simulate the sending of a signal
    async def simulate(self, idx):
        print(" [ Node Simulated: ] ", self.idx)
        i = self.resolution(440)
        while i > 0:
            await self.snd(self.connections[idx])
            print("|> Simulating: ", i)
            print("theta::", self.theta, ", thrsh::", self.threshold, ", recpt::", self.reception)
            i -= 1