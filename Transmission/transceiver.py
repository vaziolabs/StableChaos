import asyncio

# Node class
    # Node has a resonator
    # Node has a threshold
    # moving average or a gate .. or a combination of both

def clamp(n):
    return int(min(max(int(n), -255), 255))

class Transceiver:
    def __init__(self):
        print("Transceiver initialized")
        self.latency = 0.1              # Latency is the timestep between intervals, e.g. our 'potential' to receive a transmission, our real frequency
        self.resonation = 0.0           # resonation is our 'held' frequency, the potential to be transmitted e.g. "hz"
        self.threshold = 0              # Threshold is a int between -255 and 255 == 511 values, because 0 is UNIFORM or Neutral
        self.reception = 0              # Reception is the frequency we are receiving, e.g. the frequency we are receiving
        self.transceivers = []       # This is a set of all the transceivers we are connected to
    
    async def resonate(self):
        print("Resonating")

        # If we are positive,
        if self.resonation >= 0: 
            # If our threshold is less than our resonation, 
            if self.threshold < self.resonation:
                # add the difference of the threshold and the reception to our resonation
                self.resonation += self.reception - self.threshold
                # recalculate our threshold
                self.threshold = (self.threshold + self.resonation) / self.latency
            # If our threshold is above our resonation,
            else:
                # if our reception is less than our threshold, 
                if self.reception < self.threshold:
                    difference = self.threshold - self.reception
                    self.resonation += difference
                    self.threshold = self.threshold - difference / 2
                # otherwise
                else:
                    # we add the difference of the reception and the threshold to our resonation
                    difference = self.reception - self.threshold
                    self.resonation += difference
                    self.threshold = (self.threshold + self.resonation) / self.latency
        # If we are negative,
        else:
            # If our threshold is less than our resonation, 
            if self.threshold < self.resonation:
                # add the difference of the threshold and the reception to our resonation
                self.resonation -= self.threshold - self.reception
                # recalculate our threshold
                self.threshold = (self.threshold + self.resonation) / self.latency
            # If our threshold is above our resonation,
            else:
                # if our reception is less than our threshold, 
                if self.reception < self.threshold:
                    difference = self.threshold - self.reception
                    self.resonation += difference
                    self.threshold = self.threshold - difference / 2
                # otherwise
                else:
                    # we add the difference of the reception and the threshold to our resonation
                    difference = self.reception - self.threshold
                    self.resonation += difference / 2.0
                    self.threshold = (self.threshold + self.resonation) / self.latency
                    
        # If we get here, we need to resonate within our threshold, and begin to 0 out our resonation
        self.resonation = self.resonation + (self.threshold - self.resonation) / self.latency
        self.threshold = clamp(self.threshold + (self.resonation - self.threshold) / self.latency)

        for transceiver in self.transceivers:
            await self.transmit(self)


    async def transmit(self, other):
        print("Transmitting")
        await other.receive(self)
        asyncio.sleep(self.latency)

    # This is an accessor through our own transmission implementation
    async def receive(self, transmission):
        if transmission not in self.transceivers:
            self.transceivers.append(transmission)
        self.reception = transmission.resonation
        print("Received: ", self.reception)
        return await self.resonate()