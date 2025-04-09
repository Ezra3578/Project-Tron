# Proyecto-Tron

--------------------------------------------------------------------------------------------------------------------------------------------------------------
GOAL

The goal of this project is to create a simulation where two smart agents play a Tron-style game using multi-agent reinforcement learning (MARL). In this simulation, the agents make decisions in real time. They do this by detecting collisions, following light trails, and using updated map information, which is stored in a multi-channel matrix (tensor).

--------------------------------------------------------------------------------------------------------------------------------------------------------------
TECHNOLOGIES

The system uses different technologies and libraries:

Pygame for showing the game, handling events, controlling time, and using the keyboard.

NumPy for working with arrays, and data manipulation and development of Q-tables.

Matplotlib to visualize the metrics, such as the rewards and politics of the agents.

Petting Zoo with SuperSuit to create the multiplayer environment and process it.

MARLlib to use multi-agent learning algorithms.

PyTorch to include the Self-Play Technique.

--------------------------------------------------------------------------------------------------------------------------------------------------------------
PROJECT DISTRIBUTION

The project has different parts:

Main.py: Starts the game loop.

Game.py: Main class for game logic, including drawing, collisions, and updating states.

Player.py: Handles player movement and drawing the light trail.

Config.py: Manages game sounds and graphics.

Environment.py: Prepares the training environment with Petting Zoo, SuperSuit, and the RL tools.

--------------------------------------------------------------------------------------------------------------------------------------------------------------
CIBERNETIC COMPONENTS

Agents get sensor inputs (like collisions, positions, directions, and trails) in a 3D matrix.
They can move in four directions (up, down, left, right). 
The reward system gives +1 for every second alive, +10 when the opponent crashes, and −10 if the agent crashes. This helps the agents learn both attack and defense strategies.
