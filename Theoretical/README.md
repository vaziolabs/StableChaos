# Sine
 Represents implementing Asin(2πft+ϕ)

# Angular Phase
 Represents forward and backwards movement in phases regarding frequency and waveform

# Superposition
 To analyze the direction of the resultant wave (superposition of two waves moving in opposite directions), we can calculate the phase velocity and group velocity. These concepts help determine how the wave energy propagates over time. Here’s how we can modify the previous example in Python to include calculations for phase velocity and group velocity:

 - **Wave 1 (`wave1_forward`)**: Represents a sine wave moving forward in time with amplitude \(A_1\), frequency \(f_1\), and phase shift \(\phi_1\).
 - **Wave 2 (`wave2_backward`)**: Represents a sine wave moving backward in time with parameters \(A_2\), \(f_2\), \(\phi_2\)
 - **Combined Wave (`combined_wave`)**: Superposition of both waves (`wave1_forward` + `wave2_backward`).

# EMFP
 An Attempting at expressing an abstraction of Electromagnetic Wave Parameters

1. **Wavelength Calculation:**
    - The wavelength is calculated by dividing the speed of light (\(c\)) by the frequency (\(f\)) of the electromagnetic wave.

   \[
   \lambda = \frac{c}{f}
   \]
   - \(\lambda\): Wavelength (m)
   - \(c\): Speed of light (\(3 \times 10^8\) m/s)
   - \(f\): Frequency (Hz)

2. **Gaussian Pulse:**
    - The Gaussian pulse represents the initial shape of the pulse, where \(A\) is the amplitude, \(X\) is the distance, and \(\lambda\) is the wavelength.

   \[
   \text{gaussian\_pulse} = A \exp \left(-\left(\frac{X}{\lambda}\right)^2\right)
   \]
   - \(A\): Amplitude (V/m)
   - \(X\): Distance (m)
   - \(\lambda\): Wavelength (m)

3. **Electric Field Calculation:**
    - The electric field is derived by multiplying the Gaussian pulse with a cosine function. This models the wave propagation over space (\(X\)) and time (\(T\)), with frequency \(f\) and speed of light \(c\).

   \[
   E(X, T) = \text{gaussian\_pulse} \cdot \cos \left(2 \pi f \left(\frac{X}{c} - T\right)\right)
   \]
   - \(E\): Electric field (V/m)
   - \(f\): Frequency (Hz)
   - \(X\): Distance (m)
   - \(T\): Time (s)

4. **Absorbed Energy:**
    - The absorbed energy is calculated by multiplying the square of the electric field (\(E\)) with the absorption coefficient (\(\alpha\)). This gives the energy absorbed by the medium.

   \[
   \text{absorbed\_energy} = \alpha \cdot E^2
   \]
   - \(\alpha\): Absorption coefficient (\(0.1 \, \text{m}^{-1}\))
   - \(E\): Electric field (V/m)

5. **Magnetic Field Calculation:**
    - The magnetic field is computed by taking the square root of the absolute value of the electric field divided by the permeability of free space (\(\mu_0\)), and then multiplying by a sine function. This models the magnetic field associated with the propagating electromagnetic wave.

   \[
   H(X, T) = \sqrt{\frac{|E|}{4 \pi \times 10^{-7}}} \cdot \sin \left(2 \pi f \left(\frac{X}{c} - T\right)\right)
   \]
   - \(H\): Magnetic field (A/m)
   - \(|E|\): Magnitude of the electric field (V/m)
   - \(\mu_0\): Permeability of free space (\(4 \pi \times 10^{-7} \, \text{H/m}\))
