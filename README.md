# IdleShutdown

Shutdown after a set amount of minutes or hours of idle time.

## Description

IdleShutdown is a Python script that monitors system idle time and automatically shuts down your computer after a specified period. It displays a GUI window with a countdown timer showing the remaining time until shutdown.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- Windows (uv downloads the project's Python version automatically)

## Setup

Double-click `install.bat` to create the project environment and install the development tools. You can also run `uv sync` from the project folder.

## Usage

### Command Line Mode

Run the script with a time argument:

```bash
start.bat 30m
```

Or run it directly through uv:

```bash
uv run python main.py 30m
```

**Time Format:**
- `m` for minutes (e.g., `60m` = 60 minutes)
- `h` for hours (e.g., `2h` = 2 hours)

**Examples:**
```bash
start.bat 30m    # Shutdown after 30 minutes
start.bat 2h     # Shutdown after 2 hours
start.bat 90m    # Shutdown after 90 minutes
```

With a command line argument, the script relaunches with the `pythonw.exe` next to the current interpreter, so it uses the uv environment's Python rather than a system Python on PATH.

### Interactive Mode

Run without arguments to enter interactive mode:

```bash
start.bat
```

You'll be prompted to enter the time:
```
Enter time to wait before shutdown (e.g., 60m for 60 minutes, 2h for 2 hours):
```

## Tests

Run the unit tests with:

```bat
tools\run_tests.bat
```

## Update

Double-click `update.bat` to update the locked dependencies, sync the environment, and run linting, type checking, and tests.

## Features

- **Countdown Timer**: Displays remaining time in a GUI window
- **Window Title Updates**: Shows countdown in the window title (minutes when >60s, seconds otherwise)
- **Idle Time Monitoring**: Resets the timer if user activity is detected (idle time < 2 seconds)
- **Forced Shutdown**: Uses Windows shutdown command with force flag (`shutdown /s /f /t 0`)
- **Hidden Console**: When launched with command line arguments, runs without showing a console window
