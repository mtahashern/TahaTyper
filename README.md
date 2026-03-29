# TahaTyper - Professional Auto Typer

TahaTyper is a desktop application designed to simulate human-like keyboard input. It's perfect for automating repetitive typing tasks with a natural touch.

## Features
- **Custom Text Input**: Type any text you want automatically.
- **Adjustable Speed**: Control the typing speed from 10ms to 300ms per key.
- **Human-Like Simulation**:
  - **Randomized Delays**: Mimics the natural rhythm of human typing.
  - **Punctuation Pauses**: Adds slight pauses after periods, commas, and line breaks.
  - **Simulated Mistakes**: Occasionally makes a mistake and corrects it with a backspace.
- **Global Hotkeys**:
  - **F6**: Start typing (after a 3-second countdown).
  - **F7**: Emergency stop typing.
- **Loop Mode**: Repeat the typing sequence indefinitely.
- **Sleek UI**: Modern dark theme with intuitive controls.

## How to Use
1. Enter the text you want to be typed in the text box.
2. Adjust the speed and toggle any human-like behaviors you want.
3. Click **START** or press **F6**.
4. You have 3 seconds to switch to the application where you want the text to appear.
5. To stop at any time, click **STOP** or press **F7**.

## Technical Requirements
- Python 3.x
- Libraries: `pynput`, `keyboard`, `tkinter`

## Installation
If you are running from source:
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python TahaTyper.py`
