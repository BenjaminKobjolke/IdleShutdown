import ctypes
import os
import sys
import time
import tkinter as tk

# Define a structure for the last input info (for Windows)
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_uint)]

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

def update_countdown(label, start_time, wait_time, root):
    current_idle_time = get_idle_time()
    elapsed_time = time.time() - start_time
    remaining_time = max(wait_time - elapsed_time, 0)

    if current_idle_time < 2:  # Reset timer if there's user activity
        start_time = time.time()

    formatted_time = format_time(remaining_time)
    label.config(text=f"Time remaining until shutdown: {formatted_time}.")

    if remaining_time <= 0:
        root.quit()  # Exit the Tkinter mainloop
        shutdown()
    else:
        root.after(1000, update_countdown, label, start_time, wait_time, root)  # Update every second

def main():
    input_time = input("Enter time to wait before shutdown (e.g., 60m for 60 minutes, 2h for 2 hours): ")
    try:
        if input_time.endswith('m'):
            wait_time = int(input_time[:-1]) * 60
        elif input_time.endswith('h'):
            wait_time = int(input_time[:-1]) * 3600
        else:
            print("Invalid input format. Use 'm' for minutes or 'h' for hours.")
            sys.exit(1)
    except ValueError:
        print("Invalid number.")
        sys.exit(1)

    start_time = time.time()
    root = tk.Tk()
    root.title("Shutdown Timer")
    label = tk.Label(root, text="", padx=20, pady=20)
    label.pack()

    # Initialize countdown update
    update_countdown(label, start_time, wait_time, root)

    root.mainloop()

if __name__ == "__main__":
    main()
