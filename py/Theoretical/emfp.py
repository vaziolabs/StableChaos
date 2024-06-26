import numpy as np
import matplotlib.pyplot as plt

# Electromagnetic wave parameters
sample_rate = 44100  # Hz
frequency = 15e9  # Hz
speed_of_light = 3e8  # m/s
wavelength = speed_of_light / frequency  # m
amplitude = 2.0  # V/m

# Medium parameters
absorption_coefficient = 0.1  # m^-1

# Simulation parameters
duration = frequency / 2 # s
distance = wavelength * 2  # m

# Generate space and time arrays
space = np.linspace(0, distance, 1000)
time = np.linspace(0, duration, 1000)

# Create a 2D grid of space and time
X, T = np.meshgrid(space, time)

# Define the Gaussian pulse
gaussian_pulse = amplitude * np.exp(-(X / wavelength) ** 2)

# Calculate the electric field
electric_field = gaussian_pulse * np.cos(2 * np.pi * frequency * (X / speed_of_light - T))

# Calculate the absorption
absorbed_energy = absorption_coefficient * electric_field ** 2

# Calculate the magnetic field (assuming vacuum with μ_0 = 4π x 10^-7 H/m)
magnetic_field = np.sqrt(np.abs(electric_field) / (4 * np.pi * 1e-7)) * np.sin(2 * np.pi * frequency * (X / speed_of_light - T))
#magnetic_field = -np.sqrt(np.abs(electric_field) / (4 * np.pi * 1e-7)) * np.sin(2 * np.pi * frequency * (X / speed_of_light - T)) // This is the negative version of the magnetic field

# Plot the electric field, magnetic field, and absorption
plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.imshow(electric_field, extent=[0, distance, 0, duration], origin='lower', aspect='auto',
           cmap='viridis', label='Electric Field')
plt.xlabel('Distance (m)')
plt.ylabel('Time (s)')
plt.title('Electric Field Propagation')

plt.subplot(2, 2, 2)
plt.imshow(magnetic_field, extent=[0, distance, 0, duration], origin='lower', aspect='auto',
           cmap='viridis', label='Magnetic Field')
plt.xlabel('Distance (m)')
plt.ylabel('Time (s)')
plt.title('Magnetic Field Propagation')

plt.subplot(2, 2, 3)
plt.imshow(absorbed_energy, extent=[0, distance, 0, duration], origin='lower', aspect='auto',
           cmap='hot', label='Absorbed Energy')
plt.xlabel('Distance (m)')
plt.colorbar(label='Absorbed Energy Density (V^2/m^2)')
plt.title('Absorption of Electric Field')

plt.tight_layout()
plt.show()