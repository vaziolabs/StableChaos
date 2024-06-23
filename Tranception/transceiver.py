import asyncio
import math
import random

# Node class
    # Node has a resonator
    # Node has a threshold
    # moving average or a gate .. or a combination of both

SAMPLE_FREQUENCY = 44100

atan2 = lambda x: math.degrees(math.atan2(x[0], x[1])) 
sincos = lambda omega: (math.sin(omega), math.cos(omega))

class Transceiver:
    def __init__(self, threshold=1.0):
        # This resolution lambda gives us the ability to calculate the number of samples
        # needed to reach a certain frequency e.g. sample_size
        self.resolution = lambda offset: int(SAMPLE_FREQUENCY / offset)

        self.omega = 2 * math.pi / SAMPLE_FREQUENCY # This is the frequency, in radians
        self.phase = (0.0, 0.0)     # This is the phase of the wave, in radians
        self.theta = 90.0           # This is the angle of the wave defined by the phase, in degrees
        self.threshold = threshold
        self.reception = 0.0 
        print(" - Transceiver initialized")

    # This function gives us a tail by building our tangent with 
    # the sinusoidal wave where the threshold tails theta in it's resonance
    def wave(self):
        self.omega = 2 * math.pi * self.resolution(self.threshold)
        self.phase = sincos(self.omega)
        self.theta = atan2(self.phase) # This is observed in degrees

    async def resonate(self):
        self.wave()

        print(" > Beginning resonance:\t"
                f"theta::{self.theta:.5f}\t"
                f"thrsh::{self.threshold:.5f}\t"
                f"recpt::{self.reception:.5f}\t")
        
        # If we are positive,
        if self.theta >= 0: 
            # If our threshold is less than our theta, 
            if self.threshold <= self.theta:
                # add the difference of the threshold and the reception to our theta
                self.theta += self.reception - self.threshold
                # recalculate our threshold
                self.threshold = (self.threshold + self.theta) / SAMPLE_FREQUENCY
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
                    self.threshold = (self.threshold + self.theta) / SAMPLE_FREQUENCY
        # If we are negative,
        else:
            # If our threshold is less than our theta, 
            if self.threshold < self.theta:
                # add the difference of the threshold and the reception to our theta
                self.theta -= self.threshold - self.reception
                # recalculate our threshold
                self.threshold = (self.threshold + self.theta) / SAMPLE_FREQUENCY
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
                    self.threshold = (self.threshold + self.theta) / SAMPLE_FREQUENCY
                    
        # If we get here, we need to resonate within our threshold, and begin to 0 out our theta
        #self.theta = self.theta + (self.threshold - self.theta) / self.latency
        self.threshold = self.threshold + (self.theta - self.threshold) / SAMPLE_FREQUENCY
        return self.theta