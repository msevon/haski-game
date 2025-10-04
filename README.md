# Haski Platform Game

A simple platformer game made using PyQt5.

## Game Overview

Haski is a 2D platformer game where you control a husky character through various levels. Collect beers, avoid enemies and obstacles, and reach the goal as quickly as possible!

## Repository Structure

### `/src`
- **`/corruptlevels`**: Corrupted level files used in unittests
- **`/levels`**: All playable levels in the game
- **`/resources`**: All the resources (player, enemies, blocks) used in the game
- **`/sounds`**: Sounds and music used in the game
- **`/sprites`**: All the sprites used in the game
- **`constantVariables.py`**: Constant variables used in the game
- **`exceptions.py`**: Exceptions
- **`gui.py`**: The graphical user interface used in the game
- **`levelRenderer.py`**: Renders the levels
- **`menus.py`**: Menus used in the game
- **`play.py`**: Main game entry point
- **`scene.py`**: The scene used in the game
- **`session.py`**: Game session used in the game
- **`tests.py`**: Unittests for the game
- **`utils.py`**: Helper functions and classes

## Installation

### Prerequisites

You need Python 3.6 or higher and PyQt5 to run this game.

### Step 1: Install Python

Download and install Python from the official website:
- **Windows/Mac/Linux**: https://www.python.org/downloads/

### Step 2: Install PyQt5 using pip

Open your terminal/command prompt and run:

```bash
pip install PyQt5
```

**Alternative installation methods:**

```bash
# If you have multiple Python versions
pip3 install PyQt5

# If you're using conda
conda install pyqt

# If you need to upgrade pip first
python -m pip install --upgrade pip
pip install PyQt5
```

### Step 3: Verify Installation

```bash
python -c "import PyQt5; print('PyQt5 installed successfully!')"
```

## How to Play

### Running the Game

1. Navigate to the game directory using the terminal:

```bash
cd path/to/haski-game
```

2. Run the game:

```bash
python play.py
```

### Game Controls

- **Arrow Keys**: Move left/right
- **Spacebar**: Jump
- **R**: Retry current level
- **M**: Return to main menu
- **P**: Pause/Resume

### Gameplay

1. Press "Play" in main menu
2. Choose a level from the selection screen
3. Control your husky character with arrow keys
4. Jump with spacebar to avoid obstacles
5. Collect beers for points (but they make you "drunk" with visual effects!)
6. Avoid enemies and lava - they will kill you!
7. Reach the green goal flag to complete the level
8. Try to finish as quickly as possible for better scores

## Testing

Run the test suite to verify everything works correctly:

```bash
python tests.py
```

## Graphics

All graphics were created using Piskel: https://www.piskelapp.com/

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'PyQt5'"**
```bash
pip install PyQt5
```

**"python is not recognized"**
- Make sure Python is installed and added to your PATH
- Try using `python3` instead of `python`

**Game won't start**
- Check that all files are in the correct directories
- Make sure you're running from the correct directory
- Check the console for error messages

## Development

### Running Tests

```bash
# Run all tests
python tests.py

# Run specific test (if available)
python -m pytest tests/
```

### Project Structure

The game follows a modular structure:
- **GUI**: Handles the main window and graphics
- **Scene**: Manages the game world and objects
- **Session**: Controls game logic and timing
- **Resources**: Contains all game objects (player, enemies, items)
- **Levels**: Text-based level files that get parsed into game objects

## License

MIT.