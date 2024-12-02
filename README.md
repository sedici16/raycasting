# Raycasting Game Engine with Pygame

This project is a **2D raycasting-based game engine** built using **Pygame**, offering a simple simulation of a 3D environment within a 2D grid. It includes dynamic lighting, collision detection, and interactive player controls. The engine demonstrates foundational game development concepts like rendering, raycasting, and grid-based maps.

## Features

### 1. **Raycasting Engine**
- Casts rays from the player’s position to simulate a 3D environment.
- Dynamically calculates wall distances for realistic depth effects.
- Supports adjustable **Field of View (FOV)** and player-controlled rotation.

### 2. **Player Movement**
- Smooth movement with **collision detection** against walls.
- Rotational controls allow players to explore the environment.

### 3. **Grid-Based Map**
- 2D grid layout with walls and open spaces defined by a map array.
- Walls rendered using textures for visual realism.

### 4. **Rendering System**
- Wall heights adjusted dynamically based on player distance.
- Separate rendering layers for walls, ceilings, and floors.
- Dynamic shading effects for depth perception.

### 5. **Game Architecture**
- Organized with classes for modular design:
  - **`Player`**: Handles movement and rotation logic.
  - **`RayCaster`**: Casts rays and renders walls dynamically.
  - **`GameMap`**: Manages the grid-based map and boundaries.
  - **`Game`**: Main loop to manage inputs, rendering, and logic.

## Getting Started

### Prerequisites
- Python 3.x
- Pygame library
  ```bash
  pip install pygame
