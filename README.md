# IdleShutdown
Shutdown after a set amount of minutes or hours of idletime

## Description
IdleShutdown is a Python script that monitors system idle time and automatically shuts down your computer after a specified period. It displays a GUI window with a countdown timer showing the remaining time until shutdown.

## Requirements
- Python 3.x
- tkinter (usually included with Python)
- Windows OS (uses Windows API for idle time detection)

## Usage

### Command Line Mode
Run the script with a time argument:

```bash
python main.py <time>
```

**Time Format:**
- `m` for minutes (e.g., `60m` = 60 minutes)
- `h` for hours (e.g., `2h` = 2 hours)

**Examples:**
```bash
python main.py 30m    # Shutdown after 30 minutes
python main.py 2h     # Shutdown after 2 hours
python main.py 90m    # Shutdown after 90 minutes
```

**Note:** When using command line arguments, the script automatically relaunches using `pythonw.exe` to hide the console window.

### Interactive Mode
Run the script without arguments to enter interactive mode:

```bash
python main.py
```

You'll be prompted to enter the time:
```
Enter time to wait before shutdown (e.g., 60m for 60 minutes, 2h for 2 hours):
```

## Features
- **Countdown Timer**: Displays remaining time in a GUI window
- **Window Title Updates**: Shows countdown in the window title (minutes when >60s, seconds otherwise)
- **Idle Time Monitoring**: Resets the timer if user activity is detected (idle time < 2 seconds)
- **Forced Shutdown**: Uses Windows shutdown command with force flag (`shutdown /s /f /t 0`)
- **Hidden Console**: When launched with command line arguments, runs without showing a console window
