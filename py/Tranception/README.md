# Tranception Evokation System

### Intent 
An attempt to create a highly scalable abstract type that can have infinite transitory states, and self-defining relationships. We have acheived a set of first principle rules that allow us to define a simple data type that produces the type of adjacency matrix seen below, with multiple orders of connectivity and feedback across a very simple network, constructed with a simple set of rules with mechanisms to calculate resonance, threshold, induction and interference, as well as phase and theta.

The system analyzes how waves interact between nodes to minimize signal overlap, maximize efficiency, and detect areas of signal concentration or divergence in networks.

This has the potential to beused to optimize communication reliability in wireless networks, enhance signal detection in sensor arrays, improve antenna beamforming, ensure electromagnetic compatibility in electronic devices, and even advance quantum computing by optimizing qubit interactions. This borders being evidence for proofs in string and quantum theory, as well as having pieces of platonic solids, sacred geometry and even the Kabbalah.

 t scale, it could enable large-scale distributed network management, enhances system efficiency, and supports real-world applications such as wireless communications, environmental monitoring, acoustic systems optimization, and quantum network operations.


### Model
```
Green - Origin
Red - Orthogonal
Green - Adjacent
Black - Polar
```
A Single Nodes connections
![image](https://github.com/BigStickStudio/StableChaos/assets/87874714/37af4ce5-b436-48db-8fea-d80c2cfb9262)

Fully Connected (all surrounding reflections)
![image](https://github.com/BigStickStudio/StableChaos/assets/87874714/77c2bd0e-bcee-4e17-87ba-9db02cdae66a)

### Overview
The Tranception Evokation System is designed to simulate and manage cognitive processes through the manipulation of oscillatory phases (theta), frequencies (omega), and resolutions. This system leverages transceivers (reflectors) to receive, process, and transmit information, enhancing communication and interaction within the network.

The system is scientifically significant due to its ability to precisely calculate and manipulate oscillatory phases (theta), frequencies (omega), and resolutions. These capabilities are crucial for optimizing signal processing and understanding cognitive dynamics.

The question is, can we use this to represent different models of physical existence, cognition, or for procedural generative and machine learning purposes?

### Usage

 - The `Tranception` model can be ran from the parent directory with `python main.py`.
    - Debug Levels can be set in debug.py
        - 5 is most verbose and 0 is most silent
    - Dimensionality can be set in main.py
        - Linear, Planar and Cubic are currently supported.

### Todos:
 - [ ] Implement a proper debugger
 - [X] stabilize and scale the transceiver model to ensure functional integrity
 - [ ] Implement Configurations and Dimensions such that we can acheive
    - [ ] Dimensionality
        - [X] 1x2 - Linear
        - [X] 2x2 - Planar
        - [X] 3x3x3 - Cubic
            - [ ] - with Toroidal/Spherical connections
        - [ ] 3x3x3x2 - Tensor 
    - [ ] Configuration
        - [ ] Sparse - Orthogonal Only
        - [ ] Radial - Adjacent Only
        - [ ] Contiguous - Orthogonal and Adjacent Only
        - [ ] Polar - Only Polar Connections
        - [ ] Mesh - Complete
        - [ ] Toroidal - Complete + Infinite bounds e.g. (max_width)-(0)
        - [ ] Hyper - Everything connected to everything else.
    - [ ] Directionality
        - [ ] Forward
        - [ ] Backwards
        - [ ] Radio
 - [ ] add the ability to view, or phase step based on the reflection type
 - [ ] add the ability to integrate filters
 - [ ] add functionality for audio, electrical and electromagnetic analysis
 - [ ] integrate a convolution form
 - [ ] integrate a particle like system to represent data tranception between nodes
 - [ ] implement unit tests
 - [ ] implement a dynamic ability to define theta externally
