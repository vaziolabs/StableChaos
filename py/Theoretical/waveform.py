import numpy as np

class Waveform:
    def __init__(self, amplitude=1, frequency=1, phase=0):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def generate_waveform(self, time_interval, sample_rate):
        t = np.linspace(0, time_interval, int(sample_rate * time_interval), endpoint=False)
        waveform = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
        return t, waveform

    def plot_waveform(self, time_interval, sample_rate):
        t, waveform = self.generate_waveform(time_interval, sample_rate)
        import matplotlib.pyplot as plt
        plt.plot(t, waveform)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Waveform')
        plt.grid(True)
        plt.show()

    def add_waveform(self, other):
        if self.frequency != other.frequency:
            raise ValueError("Waveforms must have the same frequency to be added.")
        new_amplitude = self.amplitude + other.amplitude
        new_phase = np.arctan2(self.amplitude * np.sin(self.phase) + other.amplitude * np.sin(other.phase),
                               self.amplitude * np.cos(self.phase) + other.amplitude * np.cos(other.phase))
        return Waveform(amplitude=new_amplitude, frequency=self.frequency, phase=new_phase)

    def subtract_waveform(self, other):
        if self.frequency != other.frequency:
            raise ValueError("Waveforms must have the same frequency to be subtracted.")
        new_amplitude = self.amplitude - other.amplitude
        new_phase = np.arctan2(self.amplitude * np.sin(self.phase) - other.amplitude * np.sin(other.phase),
                               self.amplitude * np.cos(self.phase) - other.amplitude * np.cos(other.phase))
        return Waveform(amplitude=new_amplitude, frequency=self.frequency, phase=new_phase)

    def multiply_waveform(self, other):
        if self.frequency != other.frequency:
            raise ValueError("Waveforms must have the same frequency to be multiplied.")
        new_amplitude = self.amplitude * other.amplitude
        new_phase = self.phase + other.phase
        return Waveform(amplitude=new_amplitude, frequency=self.frequency, phase=new_phase)

    def divide_waveform(self, other):
        if self.frequency != other.frequency:
            raise ValueError("Waveforms must have the same frequency to be divided.")
        new_amplitude = self.amplitude / other.amplitude
        new_phase = self.phase - other.phase
        return Waveform(amplitude=new_amplitude, frequency=self.frequency, phase=new_phase)

import unittest

class TestWaveform(unittest.TestCase):
    def test_waveform_properties(self):
        sample_rate=44100
        waveform = Waveform(amplitude=2, frequency=440, phase=np.pi/4)
        t, generated_waveform = waveform.generate_waveform(time_interval=1, sample_rate=sample_rate)

        # Check if the generated waveform has the correct amplitude
        max_amplitude = np.max(np.abs(generated_waveform))
        self.assertAlmostEqual(max_amplitude, waveform.amplitude, places=6)

        # Check if the generated waveform has the correct frequency
        freq_estimate = np.fft.fftfreq(len(generated_waveform), d=1/sample_rate)
        fft_result = np.abs(np.fft.fft(generated_waveform))
        self.assertEqual(np.argmax(fft_result), np.argmax(freq_estimate == waveform.frequency))

        # Check if the generated waveform has the correct phase
        reference_waveform = waveform.amplitude * np.sin(2 * np.pi * waveform.frequency * t + waveform.phase)
        self.assertTrue(np.allclose(generated_waveform, reference_waveform, atol=1e-6))

if __name__ == '__main__':
    unittest.main()