import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 2*np.pi, 1000)

# Parameters for Wave 1 (moving forward)
A1 = 1         # Amplitude of Wave 1
f1 = 1         # Frequency of Wave 1 (in Hz)
phi1 = 0       # Phase shift of Wave 1
wave1_forward = A1 * np.sin(2 * np.pi * f1 * t + phi1)

# Parameters for Wave 2 (moving backward)
A2 = 0.5       # Amplitude of Wave 2
f2 = 2         # Frequency of Wave 2 (in Hz)
phi2 = np.pi   # Phase shift of Wave 2 (180 degrees)
wave2_backward = A2 * np.sin(2 * np.pi * f2 * t + phi2)

# Combined Wave (superposition)
combined_wave = wave1_forward + wave2_backward

# Calculate phase velocity and group velocity
phase_velocity = (f1 * f2) / (f1 + f2)
group_velocity = (f1 - f2) / (f1 + f2)

# Plotting
plt.figure(figsize=(12, 8))

# Wave 1 (moving forward)
plt.subplot(3, 1, 1)
plt.plot(t, wave1_forward, label='Wave 1 (Forward)')
plt.title('Wave 1: Moving Forward')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

# Wave 2 (moving backward)
plt.subplot(3, 1, 2)
plt.plot(t, wave2_backward, label='Wave 2 (Backward)')
plt.title('Wave 2: Moving Backward')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

# Combined wave (superposition)
plt.subplot(3, 1, 3)
plt.plot(t, combined_wave, label='Combined Wave')
plt.title('Superposition of Waves')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

# Print velocities
plt.text(0.5, 0.2, f'Phase Velocity: {phase_velocity:.2f} Hz\nGroup Velocity: {group_velocity:.2f} Hz', ha='center', va='center', transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))

plt.tight_layout()
plt.show()