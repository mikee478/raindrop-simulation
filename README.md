# 2D Raindrop Simulation

The 2D Raindrop Simulation project is a captivating, yet simple implementation of water dynamics, based on Hugo Elias' article titled "2D Water." This simulation offers a mesmerizing visual representation of raindrops interacting with a 2D grid that represents the water's height at various locations. What makes this simulation unique is its ability to achieve realistic water movement without the use of trigonometric functions or differential equations.

At its core, the simulation employs a straightforward yet effective approach to update the water's height and simulate its behavior. The 2D grid serves as a canvas where the height of the water is depicted at each discrete location. The simulation dynamically evolves by iterating over each grid cell, recalculating the water's height based on neighboring cells and estimated velocity.

To update the water's height at a particular grid cell, the simulation computes the average height of its neighboring cells. This collective average serves as a foundation for the height update. Additionally, the simulation introduces the concept of estimated velocity, which is determined by subtracting the current height from the previous height. By incorporating this velocity component, the simulation emulates the movement and flow of water.

The utilization of the average height of neighboring cells, coupled with the estimated velocity, results in a visually striking representation of raindrop behavior. As raindrops interact with the grid, their impact creates ripples that propagate and merge with adjacent ripples, producing an intricate and captivating water simulation.

https://github.com/mikee478/raindrop-simulation/assets/28791222/4abbaecb-d766-4703-9fd2-26e8d12a4820
