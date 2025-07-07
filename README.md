# Breakout Vision Game

A unique implementation of the classic Breakout game that uses computer vision to control the paddle through a webcam. The game tracks a fluorescent green object to determine the paddle's position, offering an innovative and interactive gaming experience.

## Project Description

This project combines computer vision techniques with game development to create an engaging version of Breakout. Instead of using traditional keyboard controls, players move the paddle by moving a fluorescent green object in front of their webcam. The system tracks this object in real-time using various computer vision methods:

- HSV color segmentation
- Contour detection
- Mean-shift tracking
- Gradient-based object detection

## Requirements

- Python 3.x
- Webcam
- Fluorescent green object (card, paper, or any object with similar color)
- PyCharm IDE

## Installation Guide

### 1. Install PyCharm

1. Visit the [PyCharm download page](https://www.jetbrains.com/pycharm/download/)
2. Download and install PyCharm Community Edition (free) for your operating system
3. Follow the installation wizard instructions

### 2. Clone the Project

1. Open PyCharm
2. Click on `Get from VCS` on the welcome screen (or `File > New > Project from Version Control`)
3. Paste the repository URL 👉 https://github.com/papitalos/breakout-vision.git
4. Click `Clone`

### 3. Set Up Python Environment

1. Open the project in PyCharm
2. Go to `File > Settings > Project > Python Interpreter`
3. Click on the gear icon and select `Add`
4. Choose `Conda Environment` > `New environment`
5. Select Python version 3.x
6. Click `OK` to create the environment

### 4. Install Dependencies

Open the terminal in PyCharm (View > Tool Windows > Terminal) and run:

```bash
  pip install numpy
```
```bash
  pip install opencv-python 
```
```bash
  pip install pygame
```

## Running the Game

1. Make sure your webcam is connected and working
2. Open `main.py` in PyCharm
3. Right-click in the editor and select `Run 'main'`
4. Hold a fluorescent green object in front of your webcam

### Controls

- Press `1-4` to switch between different tracking methods
- Press `q` to quit the game
- Move the green object left and right to control the paddle

### Game Modes (1-4)

1. Tracking Mode: Uses mean-shift tracking
2. Find Objects Mode: Uses gradient-based detection
3. Segmentation Mode: Uses HSV color segmentation
4. Combined Mode: Uses all methods together

## Note

A webcam is required to play the game. The tracking works best with fluorescent green objects in good lighting conditions.
