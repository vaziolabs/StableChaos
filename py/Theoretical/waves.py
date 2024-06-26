import math
import numpy as np
import matplotlib.pyplot as plt

def waveCounts(n1f, n2f, duration):
    # Calculate the number of samples for one period of the lower frequency
    total_duration = duration
    sample_count = int(sample_rate * total_duration)
    return sample_count, total_duration

def calculate_interference(combined, wave1, wave2):
    constructive_interference = combined_wave - np.maximum(wave1, wave2)
    destructive_interference = combined_wave - np.minimum(wave1, wave2)
    return -destructive_interference - constructive_interference 

def calculateDivergence(phase1, phase2):
    return np.gradient(phase1 - phase2)


def calculate_wave(amplitude, frequency, phase_shift, t):
    """Generate a sinusoidal wave."""
    return amplitude * np.sin(2 * np.pi * frequency * t + phase_shift)

def plotBothWaves(n1, n2, t):
    plt.subplot(3, 2, 1)
    plt.axhline(0, color='k', linestyle='--', linewidth=0.25)
    plt.plot(t, n1, label='Node 1')
    plt.plot(t, n2, label='Node 2')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Node Waves')
    plt.legend()

def plotCombinedWaves(combined, t):
    plt.subplot(3, 2, 2)
    plt.axhline(0, color='k', linestyle='--', linewidth=0.25)
    plt.plot(t, combined, label='Combined Wave', color='g')
    plt.title('Total Interference')
    plt.legend()

def plotInterference(interference, t):
    plt.subplot(3, 2, 3)
    plt.axhline(0, color='k', linestyle='--', linewidth=0.25)
    plt.plot(t, interference, label='Interference', linestyle='--', color='b')
    plt.title('Interference')
    plt.legend()

def plotDivergence(divergence, t):
    plt.subplot(3, 2, 4)
    plt.axhline(0, color='k', linestyle='--', linewidth=0.25)
    plt.plot(t, divergence, label='Divergence', color='r')
    plt.xlabel('Time (s)')
    plt.ylabel('Phase Difference (radians)')
    plt.title('Divergence')
    plt.legend()

def plotPhaseDifference(phase_diff, t):
    plt.subplot(3, 2, 5)
    plt.axhline(0, color='k', linestyle='--', linewidth=0.25)
    plt.plot(t, phase_diff, label='Phase Difference', color='m')
    plt.xlabel('Time (s)')
    plt.ylabel('Phase Difference (radians)')
    plt.title('Phase Difference (Interference)')
    plt.legend()

lcm = lambda a, b: abs(a*b) // math.gcd(a, b)

# Node parameters
f1 = 440  # Hz
f2 = 220  # Hz
amplitude1 = 1  # Amplitude of wave 1
amplitude2 = 0.5 

# Simulation parameters
sample_rate = 44100  # samples per second
phase_offset = np.pi / 2  # radians
phase_normal = np.arctan2(np.sin(phase_offset), np.cos(phase_offset))

# Generate time array for number of samples per period
p1 = 1 / f1
p2 = 1 / f2
lcm_period = lcm(int(p1 * sample_rate), int(p2 * sample_rate)) / sample_rate
sample_count, total_duration = waveCounts(f1, f2, lcm_period)
time = np.linspace(0, total_duration, sample_count, endpoint=False)

# Generate sine waves for each node
wave1 = calculate_wave(amplitude1, f1, 0, time)
wave2 = calculate_wave(amplitude2, f2, 0, time)
combined_wave = wave1 + wave2
phase_diff = np.angle(np.exp(1j * (wave1 - wave2)))

# Calculate phase difference
#phase_diff = np.angle(np.exp(1j * 2 * np.pi * f1 * time)) - np.angle(np.exp(1j * 2 * np.pi * f2 * time))
#phase_diff = np.degrees(phase_diff)

# Calculate constructive and destructive interference
phase1 = np.arcsin(wave1 / amplitude1)
phase2 = np.arcsin(wave2 / amplitude2) 

interference = calculate_interference(combined_wave, wave1, wave2)

# Plot the waves, interference, and phase difference
plt.figure(figsize=(12, 8))
plotBothWaves(wave1, wave2, time)
plotCombinedWaves(combined_wave, time)
plotInterference(calculate_interference(combined_wave, wave1, wave2), time)
plotDivergence(calculateDivergence(phase1, phase2), time)
plotPhaseDifference(phase_diff, time)

plt.tight_layout()
plt.show()