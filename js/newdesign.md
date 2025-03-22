<think>
I need to create a clean design document for the particle simulation application, focusing on improving the design rather than providing a technical implementation.

The current codebase shows a particle simulation system with these main components:
- App (extends Engine)
- Engine (core rendering system)
- Particles (manages collections)
- Particle (individual particles)
- Controller (manages simulation parameters)
- Topical (handles relationships)

The goal is to create a cleaner, more modular design with better separation of concerns that can handle much larger particle counts.

For a design document, I should focus on:
1. High-level architecture and components
2. Responsibilities of each component
3. Relationships between components
4. Design principles and patterns
5. Performance considerations

I'll create a clean, professional design document that focuses on these aspects rather than specific implementation details.
</think>

```markdown:newdesign.md
# Enhanced Particle Simulation System - Design Document

## Vision
Create a high-performance particle simulation system capable of rendering 100,000+ particles with complex interaction behaviors while maintaining 60+ FPS through efficient architecture and optimized rendering techniques.

## Design Goals
- Improve separation of concerns through modular architecture
- Optimize for high particle counts
- Maintain clean, extensible code structure
- Support complex particle relationships and behaviors
- Create maintainable and testable components

## System Architecture

### Core Components

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ SimulationCore  │     │ ParticleSystem  │     │   Renderer      │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  SceneManager   │     │  PhysicsEngine  │     │ InstanceManager │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │                       
                                 ▼                       
                        ┌─────────────────┐     ┌─────────────────┐
                        │ RelationshipMap │     │ ParameterManager│
                        └─────────────────┘     └─────────────────┘
```

## Component Responsibilities

### SimulationCore
- Central coordination point
- Manages simulation lifecycle
- Handles timing and frame updates
- Connects all subsystems

### SceneManager
- Manages Three.js scene
- Handles camera and viewport
- Controls scene boundaries and visuals
- Manages global scene properties

### ParticleSystem
- Stores particle data in optimized structures
- Manages particle creation and destruction
- Implements data access patterns for efficient updates
- Handles particle type assignments

### PhysicsEngine
- Processes all force calculations
- Implements spatial partitioning for efficient neighbor lookups
- Applies movement rules and boundary conditions
- Optimizes for batch processing of particles

### RelationshipMap
- Defines and manages particle type relationships
- Provides efficient lookup for attraction/repulsion values
- Handles caching of relationship calculations
- Supports complex relationship models

### Renderer
- Handles all aspects of visual presentation
- Implements efficient rendering techniques
- Manages visual effects and appearance
- Separates rendering from simulation logic

### InstanceManager
- Implements GPU instancing for efficient rendering
- Manages instance buffers and attributes
- Optimizes draw calls for large particle counts
- Handles level-of-detail strategies

### ParameterManager
- Centralizes all simulation parameters
- Provides configuration interface
- Handles parameter validation
- Manages presets and configuration persistence

## Design Improvements

### 1. Data-Oriented Architecture
- Store particle properties in typed arrays for efficient memory access
- Organize data for cache-friendly processing
- Process particles in batches rather than individually
- Separate data from behavior

### 2. Spatial Partitioning
- Implement grid-based spatial hashing
- Reduce force calculation complexity from O(n²) to O(n)
- Optimize neighbor queries for particles
- Support dynamic grid sizing based on particle density

### 3. Rendering Optimizations
- Use GPU instancing for single-draw-call rendering
- Implement shader-based particle appearance
- Support level-of-detail for distant particles
- Separate rendering from simulation logic

### 4. Modular System Design
- Clear interfaces between components
- Event-based communication for loose coupling
- Plugin architecture for extensibility
- Configuration-driven behavior

### 5. Performance-Focused Design
- Avoid garbage collection during simulation steps
- Pre-allocate memory where possible
- Use object pools for temporary objects
- Implement frame budget management

## Particle Data Management

### Optimized Data Structures
- Position data (Float32Array)
- Velocity data (Float32Array)
- Type data (Uint8Array)
- Energy data (Float32Array)
- Status flags (Uint8Array)

### Particle Types
- Defined by relationship characteristics
- Support for custom type definitions
- Type-specific behaviors and visual properties
- Configurable interaction rules

## Relationship System

### Key Concepts
- Type-based relationship mappings
- Configurable attraction/repulsion values
- Relationship categories (same, orthogonal, diagonal, polar)
- Custom bias values per particle type

### Optimizations
- Pre-computed relationship matrices
- Cached attraction values
- Efficient lookups for common cases
- Batched force applications

## Rendering System

### Performance Techniques
- Single instanced mesh for all particles
- Dynamic buffer updates
- Shader-based coloring and effects
- Culling of off-screen particles

### Visual Effects
- Particle glow based on energy
- Trail effects for movement
- Interactive highlighting
- Post-processing for enhanced visuals

## User Interface

### Simulation Controls
- Particle count adjustment
- Type relationship configuration
- Visual debugging tools
- Performance monitoring

### Visualization Tools
- Relationship strength visualization
- Type interaction diagrams
- Force field visualization
- System status indicators

## Implementation Strategy

### Phase 1: Core Architecture
- Implement basic component structure
- Define interfaces between systems
- Create foundation for data management
- Establish rendering pipeline

### Phase 2: Optimization Layer
- Implement spatial partitioning
- Add instanced rendering
- Optimize force calculations
- Implement memory management

### Phase 3: Enhanced Features
- Add advanced visual effects
- Implement additional interaction models
- Create expanded user controls
- Develop visualization tools

### Phase 4: Polish & Performance
- Optimize rendering for various devices
- Implement advanced debugging tools
- Add presets and configuration options
- Final performance tuning

## Performance Targets
- 100,000+ particles at 60+ FPS on mid-range hardware
- <16ms per frame for simulation and rendering
- <100MB memory utilization
- Smooth scaling with particle count
```