import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 1, 500, endpoint=False)

# Frequency
f = 5  # 5 Hz

# Positive frequency component (counterclockwise rotation)
positive_frequency = np.exp(1j * 2 * np.pi * f * t)

# Negative frequency component (clockwise rotation)
negative_frequency = np.exp(-1j * 2 * np.pi * f * t)

# Plotting
plt.figure(figsize=(14, 6))

# Plot positive frequency component
plt.subplot(1, 2, 1)
plt.plot(t, np.real(positive_frequency), label='Real part')
plt.plot(t, np.imag(positive_frequency), label='Imaginary part')
plt.title('Positive Frequency (5 Hz)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()

# Plot negative frequency component
plt.subplot(1, 2, 2)
plt.plot(t, np.real(negative_frequency), label='Real part')
plt.plot(t, np.imag(negative_frequency), label='Imaginary part')
plt.title('Negative Frequency (-5 Hz)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()