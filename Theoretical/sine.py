import numpy as np
import matplotlib.pyplot as plt

# Parameters
A = 1      # Amplitude
f = 1      # Frequency in Hz
phi_forward = 0    # Phase shift for forward movement
phi_backward = np.pi  # Phase shift for backward movement (180 degrees)

t = np.linspace(0, 2, 500)  # Time vector for 2 seconds

# Sine waves
y_forward = A * np.sin(2 * np.pi * f * t + phi_forward)
y_backward = A * np.sin(2 * np.pi * f * t + phi_backward)

# Plotting
plt.figure(figsize=(10, 4))

# Forward movement plot
plt.subplot(1, 2, 1)
plt.plot(t, y_forward, label=f'Forward Movement\n$\\phi={phi_forward}$')
plt.title('Sine Wave (Forward Movement)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Backward movement plot
plt.subplot(1, 2, 2)
plt.plot(t, y_backward, label=f'Backward Movement\n$\\phi={phi_backward}$')
plt.title('Sine Wave (Backward Movement)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
