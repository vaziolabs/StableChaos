import numpy as np

class Propagation:
    def __init__(self, sample_rate, frequency, speed_of_light, amplitude, absorption_coefficient, duration, distance):
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.speed_of_light = speed_of_light
        self.wavelength = speed_of_light / frequency
        self.amplitude = amplitude
        self.absorption_coefficient = absorption_coefficient
        self.duration = duration
        self.distance = distance
        self.space = np.linspace(0, self.distance, 1000)
        self.time = np.linspace(0, self.duration, 1000)
        self.X, self.T = np.meshgrid(self.space, self.time)
        self.gaussian_pulse = self.amplitude * np.exp(-(self.X / self.wavelength) ** 2)
        self.electric_field = self.gaussian_pulse * np.cos(2 * np.pi * self.frequency * (self.X / self.speed_of_light - self.T))
        self.absorbed_energy = self.absorption_coefficient * self.electric_field ** 2
        self.magnetic_field = np.sqrt(np.abs(self.electric_field) / (4 * np.pi * 1e-7)) * np.sin(2 * np.pi * self.frequency * (self.X / self.speed_of_light - self.T))
        self.propagation = np.array([self.electric_field, self.magnetic_field, self.absorbed_energy])