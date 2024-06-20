# SEngine 4
Written with Python3, NumPy, Pygame, c++ version with sfml will be soon.

This 3D Graphics Engine is a Python-based project utilizing Pygame for rendering. This project provides functionalities like perspective and orthographic projections, mouse click events, polygon clipping, and keyboard inputs for camera movement and rendering modes.

# What's new?
* New faster version of Simple Engine. 
* More optimised code, more speed and NumPy functions.
* Mostly created for N-body project

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Key Features](#key-features)
- [Keyboard Controls](#keyboard-controls)
- [Mouse Controls](#mouse-controls)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/3d-graphics-engine.git
   cd 3d-graphics-engine
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

To start the 3D Graphics Engine, run:

```sh
python main.py 1920 1080
```

You can also specify custom window dimensions:

```sh
python main.py <width> <height>
```

## Key Features

- **3D Projections**: Includes both perspective and orthographic projections.
- **Mouse Events**: Left and right mouse click actions.
- **Camera Movement**: Use keyboard inputs to move around the scene.
- **Lighting Models**: Switch between different lighting models like Lambert, Phong, Blinn, etc.

## Keyboard Controls

- **W**: Move forward
- **S**: Move backward
- **A**: Strafe left
- **D**: Strafe right
- **Q**: Move up
- **E**: Move down
- **Shift**: Increase speed
- **Ctrl**: Decrease speed
- **0-8**: Toggle between different lighting models

## Mouse Controls

- **Left Click**: Perform action (e.g., select)
- **Right Click**: Perform alternative action (e.g., context menu)
