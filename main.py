import argparse
import ctypes
import json
import os
import subprocess
import sys
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, simpledialog

SETTINGS_PATH = Path(__file__).with_name("settings.json")


# Define a structure for the last input info (for Windows)
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]


def get_idle_time():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0  # Convert milliseconds to seconds


def shutdown():
    os.system("shutdown /s /f /t 0")


def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins} minutes, {secs} seconds"


def update_countdown(label, start_time, wait_time, root, state):
    current_idle_time = get_idle_time()
    elapsed_time = time.time() - start_time
    remaining_time = max(wait_time - elapsed_time, 0)

    if current_idle_time < 2:  # Reset timer if there's user activity
        start_time = time.time()

    if remaining_time > 60:
        title = f"{int(remaining_time // 60)}m until shutdown"
    else:
        title = f"{int(remaining_time)}s until shutdown"

    root.title(title)

    formatted_time = format_time(remaining_time)
    label.config(text=f"Time remaining until shutdown: {formatted_time}.")

    if remaining_time <= 0:
        root.quit()  # Exit the Tkinter mainloop
        shutdown()
    else:
        state["after_id"] = root.after(
            1000, update_countdown, label, start_time, wait_time, root, state
        )  # Update every second


def parse_time(input_time):
    input_time = input_time.strip()
    if not input_time.endswith(("m", "h")):
        raise ValueError("Invalid input format. Use 'm' for minutes or 'h' for hours.")

    try:
        if input_time.endswith("m"):
            return int(input_time[:-1]) * 60
        return int(input_time[:-1]) * 3600
    except ValueError:
        raise ValueError("Invalid number.") from None


def load_duration(path: Path = SETTINGS_PATH) -> str | None:
    try:
        with Path(path).open(encoding="utf-8") as settings_file:
            duration = json.load(settings_file)["duration"]
        if not isinstance(duration, str):
            return None
        parse_time(duration)
        return duration
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None


def save_duration(duration: str, path: Path = SETTINGS_PATH) -> None:
    with Path(path).open("w", encoding="utf-8") as settings_file:
        json.dump({"duration": duration}, settings_file)


def ask_duration(root: tk.Tk, initial: str | None = None) -> str | None:
    while True:
        duration = simpledialog.askstring(
            "Idle shutdown",
            "Idle time before shutdown (e.g. 60m or 2h):",
            initialvalue=initial,
            parent=root,
        )
        if duration is None:
            return None
        try:
            parse_time(duration)
            return duration.strip()
        except ValueError as error:
            messagebox.showerror("Idle shutdown", str(error), parent=root)


def main():
    parser = argparse.ArgumentParser(description="Shutdown timer script.")
    parser.add_argument(
        "time",
        nargs="?",
        help="Time to wait before shutdown (e.g., 60m for 60 minutes, 2h for 2 hours)",
    )
    args = parser.parse_args()

    if args.time is not None:
        try:
            wait_time = parse_time(args.time)
        except ValueError as error:
            print(error)
            sys.exit(1)

    # Relaunch using pythonw.exe if not already running with it.
    if "pythonw.exe" not in sys.executable.lower():
        command = [
            str(Path(sys.executable).with_name("pythonw.exe")),
            __file__,
        ]
        if args.time is not None:
            command.append(args.time)
        subprocess.Popen(command)
        sys.exit(0)

    root = tk.Tk()
    root.withdraw()  # Hide the root window initially

    duration = args.time if args.time is not None else load_duration()
    if duration is None:
        duration = ask_duration(root)
        if duration is None:
            root.destroy()
            return
        save_duration(duration)
        messagebox.showinfo(
            "Idle shutdown",
            f"{duration} will now be used as the default. Use 'Change duration' in the countdown window to change it.",
            parent=root,
        )
    wait_time = parse_time(duration)

    label = tk.Label(root, text="", padx=20, pady=20)
    label.pack()

    state = {"after_id": None}
    current_duration = {"value": duration}

    def restart_countdown(new_wait_time):
        if state["after_id"] is not None:
            root.after_cancel(state["after_id"])
            state["after_id"] = None
        update_countdown(label, time.time(), new_wait_time, root, state)

    def change_duration():
        new_duration = ask_duration(root, initial=current_duration["value"])
        if new_duration is not None:
            save_duration(new_duration)
            current_duration["value"] = new_duration
            restart_countdown(parse_time(new_duration))

    tk.Button(root, text="Change duration", command=change_duration).pack()

    def show_window():
        root.deiconify()  # Show the root window
        root.state("iconic")  # Start minimized

    root.after(0, show_window)  # Show and minimize the window

    # Initialize countdown update
    update_countdown(label, time.time(), wait_time, root, state)

    root.mainloop()


if __name__ == "__main__":
    main()
