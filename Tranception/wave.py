import math
import numpy as np
import unittest
import matplotlib.pyplot as plt


least_common_multiple = lambda a, b: abs(a*b) // math.gcd(a, b)
sample_rate = 44100

class Waveform:
    def __init__(self, amplitude=1, frequency=1, phase=0):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def generateWaveform(self, time_interval, sample_rate):
        t = np.linspace(0, time_interval, int(sample_rate * time_interval), endpoint=False)
        waveform = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
        return t, waveform

    def plotWaveform(self, time_interval, sample_rate):
        t, waveform = self.generateWaveform(time_interval, sample_rate)
        import matplotlib.pyplot as plt
        plt.plot(t, waveform)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Waveform')
        plt.grid(True)
        plt.show()

    def linspaceWaveforms(self, other):
        lcm = least_common_multiple(self.frequency, other.frequency)
        t = np.linspace(0, lcm/self.frequency, int(sample_rate * lcm / self.frequency), endpoint=False)
        waveform_1 = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
        t = np.linspace(0, lcm/other.frequency, int(sample_rate * lcm / other.frequency), endpoint=False)
        waveform_2 = other.amplitude * np.sin(2 * np.pi * other.frequency * t + other.phase)
        return t, waveform_1, waveform_2
    
    def fftWaveform(self, waveform):
        fourier = np.fft.fft(waveform)
        freqs = np.fft.fftfreq(len(fourier), d=1/sample_rate)
        component = np.abs(fourier)
        max_freq_index = np.argmax(component)
        max_freq = freqs[max_freq_index]
        max_amplitude = component[max_freq_index]
        max_phase = np.angle(fourier[max_freq_index])
        return Waveform(amplitude=max_amplitude, frequency=max_freq, phase=max_phase)

    def __add__(self, other):
        waveform_1, waveform_2 = self.linspaceWaveforms(other)
        return self.fftWaveform(waveform_1 + waveform_2)


    def __sub__(self, other):
        waveform_1, waveform_2 = self.linspaceWaveforms(other)
        return self.fftWaveform(waveform_1 - waveform_2)

    def __mul__(self, other):
        waveform_1, waveform_2 = self.linspaceWaveforms(other)
        return self.fftWaveform(waveform_1 * waveform_2)
    
    def __truediv__(self, other):
        waveform_1, waveform_2 = self.linspaceWaveforms(other)
        return self.fftWaveform(waveform_1 / waveform_2)
    
    def calculateResonantFrequency(self, other):
        if self.frequency == other.frequency:
            return self.frequency
        else:
            return np.sqrt(self.frequency * other.frequency)

    def calculateReceptionLevel(self, other):
        if self.frequency == other.frequency:
            return self.amplitude * other.amplitude
        else:
            return 0.0
        

class TestWaveform(unittest.TestCase):
    def testWaveformProperties(self):
        waveform = Waveform(amplitude=2, frequency=440, phase=np.pi/4)
        t, generated_waveform = waveform.generateWaveform(time_interval=1, sample_rate=44100)

        # Check if the generated waveform has the correct amplitude
        max_amplitude = np.max(np.abs(generated_waveform))
        self.assertAlmostEqual(max_amplitude, waveform.amplitude, places=6)

        # Check if the generated waveform has the correct frequency
        freq_estimate = np.fft.fftfreq(len(generated_waveform), d=1/44100)
        fft_result = np.abs(np.fft.fft(generated_waveform))
        self.assertEqual(np.argmax(fft_result), np.argmax(freq_estimate == waveform.frequency))

        # Check if the generated waveform has the correct phase
        self.assertTrue(np.allclose(generated_waveform, waveform.amplitude * np.sin(2 * np.pi * waveform.frequency * t + waveform.phase)))

    def testWaveformAddition(self):
        waveform1 = Waveform(amplitude=2, frequency=440, phase=np.pi/4)
        waveform2 = Waveform(amplitude=3, frequency=440, phase=np.pi/2)
        waveform3 = waveform1 + waveform2
        self.assertEqual(waveform3.amplitude, 5)
        self.assertEqual(waveform3.frequency, 440)
        self.assertAlmostEqual(waveform3.phase, np.arctan2(2 * np.sin(np.pi/4) + 3 * np.sin(np.pi/2),
                                                          2 * np.cos(np.pi/4) + 3 * np.cos(np.pi/2)))

    def testWaveformSubtraction(self):
        waveform1 = Waveform(amplitude=2, frequency=440, phase=np.pi/4)
        waveform2 = Waveform(amplitude=3, frequency=440, phase=np.pi/2)
        waveform3 = waveform1 - waveform2
        self.assertEqual(waveform3.amplitude, -1)
        self.assertEqual(waveform3.frequency, 440)

    def testWaveformMultiplication(self):
        waveform1 = Waveform(amplitude=2, frequency=440, phase=np.pi/4)
        waveform2 = Waveform(amplitude=3, frequency=440, phase=np.pi/2)
        waveform3 = waveform1 * waveform2
        self.assertEqual(waveform3.amplitude, 6)
        self.assertEqual(waveform3.frequency, 440)
        self.assertAlmostEqual(waveform3.phase, np.pi/4 + np.pi/2)
    
    def testWaveformDivision(self):
        waveform1 = Waveform(amplitude=2, frequency=440, phase=np.pi/4)
        waveform2 = Waveform(amplitude=3, frequency=440, phase=np.pi/2)
        waveform3 = waveform1 / waveform2
        self.assertAlmostEqual(waveform3.amplitude, 2/3)
        self.assertEqual(waveform3.frequency, 440)
        self.assertAlmostEqual(waveform3.phase, np.pi/4 - np.pi/2)
    
    def testCalculateResonantFrequency(self):
        waveform1 = Waveform(amplitude=1, frequency=440, phase=0)
        waveform2 = Waveform(amplitude=1, frequency=440, phase=np.pi/2)
        resonant_frequency = waveform1.calculateResonantFrequency(waveform2)
        self.assertEqual(resonant_frequency, 440)

        waveform1 = Waveform(amplitude=1, frequency=440, phase=0)
        waveform2 = Waveform(amplitude=1, frequency=880, phase=np.pi/2)
        resonant_frequency = waveform1.calculateResonantFrequency(waveform2)
        self.assertEqual(resonant_frequency, 616.4414002968977)
    
    def testCalculateReceptionLevel(self):
        waveform1 = Waveform(amplitude=1, frequency=440, phase=0)
        waveform2 = Waveform(amplitude=1, frequency=440, phase=np.pi/2)
        reception_level = waveform1.calculateReceptionLevel(waveform2)
        self.assertEqual(reception_level, 1)

        waveform1 = Waveform(amplitude=1, frequency=440, phase=0)
        waveform2 = Waveform(amplitude=1, frequency=880, phase=np.pi/2)
        reception_level = waveform1.calculateReceptionLevel(waveform2)
        self.assertEqual(reception_level, 0)

    def testPlotWaveform(self):
        plt.figure(figsize=(12, 8))

        # Plot waveform properties
        waveform = Waveform(amplitude=2, frequency=440, phase=np.pi/4)
        t, generated_waveform = waveform.generateWaveform(time_interval=1/waveform.frequency, sample_rate=44100)
        plt.subplot(2, 2, 1)
        plt.plot(t, generated_waveform, label='Generated Waveform', color='red')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Waveform')

        # Parameters for add, subtract, multiply waveforms
        waveform1 = Waveform(amplitude=1, frequency=440, phase=0)
        waveform2 = Waveform(amplitude=1.5, frequency=330, phase=np.pi/2)
        lcm = least_common_multiple(waveform1.frequency, waveform2.frequency)
        time_interval = 1 / lcm

        # Plot add waveform
        t, generated_waveform = (waveform1 + waveform2).generateWaveform(time_interval=time_interval, sample_rate=44100)
        plt.subplot(2, 2, 2)
        plt.plot(t, generated_waveform, label='Sum Waveform', color='green')
        plt.plot(t, waveform1.amplitude * np.sin(2 * np.pi * waveform1.frequency * t + waveform1.phase), '--', label='Waveform 1', color='blue')
        plt.plot(t, waveform2.amplitude * np.sin(2 * np.pi * waveform2.frequency * t + waveform2.phase), '--', label='Waveform 2', color='orange')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Add Waveform')

        # Plot subtract waveform
        t, generated_waveform = (waveform1 - waveform2).generateWaveform(time_interval=time_interval, sample_rate=44100)
        plt.subplot(2, 2, 3)
        plt.plot(t, generated_waveform)
        plt.plot(t, waveform1.amplitude * np.sin(2 * np.pi * waveform1.frequency * t + waveform1.phase), '--', label='Waveform 1', color='blue')
        plt.plot(t, waveform2.amplitude * np.sin(2 * np.pi * waveform2.frequency * t + waveform2.phase), '--', label='Waveform 2', color='orange')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Subtract Waveform')

        # Plot multiply waveform
        t, generated_waveform = (waveform1 * waveform2).generateWaveform(time_interval=time_interval, sample_rate=44100)
        plt.subplot(2, 2, 4)
        plt.plot(t, generated_waveform)
        plt.plot(t, waveform1.amplitude * np.sin(2 * np.pi * waveform1.frequency * t + waveform1.phase), '--', label='Waveform 1', color='blue')
        plt.plot(t, waveform2.amplitude * np.sin(2 * np.pi * waveform2.frequency * t + waveform2.phase), '--', label='Waveform 2', color='orange')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Multiply Waveform')

        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    unittest.main()
