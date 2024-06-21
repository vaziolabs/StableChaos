import asyncio
import math
import random

# Node class
    # Node has a resonator
    # Node has a threshold
    # moving average or a gate .. or a combination of both

sample_frequency = 44100
resolution = lambda phase: int(sample_frequency / phase)

class Transceiver:
    def __init__(self, idx=0,threshold=0.0):
        print("Transceiver initialized")
        self.omega = 2 * math.pi / sample_frequency
        self.phase = (0.0, 0.0)
        self.theta = 90.0
        self.threshold = 1.0
        self.reception = 0.0 

    def wave(self):
        sin = math.sin(self.theta)
        cos = math.cos(self.theta)
        return sin, cos

    def resolve(self):
        self.omega = 2 * math.pi * resolution(self.threshold)
        
        self.phase = self.wave()
        self.theta = math.atan2(self.phase[0], self.phase[1])

    async def resonate(self):
        self.resolve()

        print("Beginning resonance")
        print("theta::", self.theta, ", thrsh::", self.threshold, ", recpt::", self.reception)
        # If we are positive,
        if self.theta >= 0: 
            # If our threshold is less than our theta, 
            if self.threshold <= self.theta:
                # add the difference of the threshold and the reception to our theta
                self.theta += self.reception - self.threshold
                # recalculate our threshold
                self.threshold = (self.threshold + self.theta) / sample_frequency
            # If our threshold is above our theta,
            else:
                # if our reception is less than our threshold, 
                if self.reception < self.threshold:
                    difference = self.threshold - self.reception
                    self.theta += difference
                    self.threshold = self.threshold - difference * 2.0
                # otherwise
                else:
                    # we add the difference of the reception and the threshold to our theta
                    difference = self.reception - self.threshold
                    self.theta += difference
                    self.threshold = (self.threshold + self.theta) / sample_frequency
        # If we are negative,
        else:
            # If our threshold is less than our theta, 
            if self.threshold < self.theta:
                # add the difference of the threshold and the reception to our theta
                self.theta -= self.threshold - self.reception
                # recalculate our threshold
                self.threshold = (self.threshold + self.theta) / sample_frequency
            # If our threshold is above our theta,
            else:
                # if our reception is less than our threshold, 
                if self.reception < self.threshold:
                    difference = self.threshold - self.reception
                    self.theta += difference
                    self.threshold = self.threshold - difference / 2.0
                # otherwise
                else:
                    # we add the difference of the reception and the threshold to our theta
                    difference = self.reception - self.threshold
                    self.theta += difference / 2.0
                    self.threshold = (self.threshold + self.theta) / sample_frequency
                    
        # If we get here, we need to resonate within our threshold, and begin to 0 out our theta
        #self.theta = self.theta + (self.threshold - self.theta) / self.latency
        self.threshold = self.threshold + (self.theta - self.threshold) / sample_frequency
        return self.theta