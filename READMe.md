# HATS - Hybrid Abstract Transitory State
## Purpose
This system is designed to model and analyze wave behavior in a network of nodes (reflectors), focusing on interference, induction, and divergence. The primary goals include:

By modeling and analyzing wave behavior in a network of nodes, we can address critical challenges in wireless communications, sensor networks, antenna arrays, acoustic systems, EMC testing, and quantum computing. Understanding interference, induction, and divergence allows for better optimization, design, and signal processing, leading to improved performance and reliability in various applications, by assessing the the net flow of wave properties (e.g., phase, amplitude) across the network, indicating areas of convergence or divergence.

This is a self-stabilizing system that leans towards certain levels of 'chaos'. This system utilizes concepts like the Uncertainty Principle to better help us define potential states through some broad and narrow assumptions.

[Tranception](https://github.com/BigStickStudio/StableChaos/tree/main/Tranception) is a model that defines rules that allow for infinite scalability based on first principals.. Defining concepts like resonance, threshold induction, interference and divergence. This allows for the emergence of self-awareness, and can be used to represent any model of anything that can be defined by a wave, or as having some flow, and could even be used for concepts like convolutions, neural networks, and basically anything that could be represented as having some geometry, volume, or fluctuation over time.

 The [Stable Chaos Model](https://github.com/BigStickStudio/StableChaos/tree/main/Stable%20Chaos%20Model) defines how a system can have an infinite number of states, be self-guiding, self-actuation, and self-stabilizing. It is a system for defining the relationship between stable systems and chaotic systems.

### Description
The core of this system has multiple components, but a single function.
 - Tranception:
    (credit to EatThePath for the simple yet powerful observation)
    One degree of freedom — a single axis and an infinite range of values.  That axis is independent from other observables. 
    
    This degree of Freedom is 2-dimensional with a potential of having 3 forms, defined by the type of connection between two resonant reflectors - but can be intrinsically observed as Theta (presently defined as `atan2(sin, cos)`). 

    We can literally observe the angle of our wave, derived from the threshold which both regulates and trails the resonance, which allows for cyclic observance over any delta.

### Usage:
 - The `Stable Chaos Model` can be ran with `python main.py`, and signifies a network of 4 nodes attempting to follow and oppose itself.
 - The `Tranception` model can be ran with `python main.py`, and simply outputs single timestep values from a given set of inputs. This diagram is far from complete.

### Todos:
 - [ ] abstract the graphics engine to allow for multiple implemetations
 - [ ] merge Stable Chaos Model annd Tranception for self stabilization amidst chaos
 - [ ] scale
 - [ ] build examples
    - [ ] audio resonance
        - [ ] audio theorem metrics for 'harmonic' evaluation
    - [ ] wave function collapse:
        - [ ] audio theorem ruleset
        - [ ] sample fft analysis for audio generation
