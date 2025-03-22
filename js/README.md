# Stable Chaos

A 3D particle simulation system built with Three.js that demonstrates emergent behaviors through simple particle interactions.

## Architecture

The application follows an object-oriented architecture with these core components:

### Components

- **Engine**: Core rendering system that manages Three.js scene, camera, and renderer
- **App**: Main application that extends Engine and initializes the particle system
- **Particles**: Manages collection of particles, their creation, removal, and updates
- **Particle**: Individual particle with physics-based behaviors and rendering

### Class Relationships

```
Engine
  ↑
  └── App
        │
        ├── Particles
        │     │
        │     └── Particle
        │
        └── Three.js components
```

## Technical Implementation

### Engine

- Manages Three.js scene, camera, renderer
- Handles window resizing
- Provides animation loop
- Manages orbit controls
- Creates bounding box visualization
- Supports pre-render callbacks

### Particles System

- Dynamically creates and removes particles
- Maintains particle count within configured limits
- Handles particle lifecycle
- Cleans up "dead" particles based on energy level and position

### Particle Physics

- Particles move with velocity vectors
- Includes basic physics simulation:
  - Repulsion forces between nearby particles
  - Energy decay over time
  - Velocity damping

## Features

- 3D particle visualization with dynamic colors
- Orbital camera controls
- Configurable particle count and limits
- Emergent behavior through simple interaction rules
- Bounded simulation space

## Usage

1. Clone the repository
2. Open index.html in a modern browser
3. Use mouse to orbit around the particle simulation:
   - Left-click + drag to orbit
   - Scroll to zoom in/out

## Technical Requirements

- Modern browser supporting ES6+ and WebGL
- No server-side requirements (runs entirely in browser)