import ctypes
import os
import sys
import time

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

    print(f"System will shutdown after {input_time} of idle time if no activity is detected.")
    start_time = time.time()

    while True:
        current_idle_time = get_idle_time()

        # If there is user activity, reset the start_time
        if current_idle_time < 2:  # Using 2 seconds to allow for small delays in detection
            start_time = time.time()

        elapsed_time = time.time() - start_time
        remaining_time = max(wait_time - elapsed_time, 0)

        formatted_time = format_time(remaining_time)
        print(f"Time remaining until shutdown: {formatted_time}.")
        #print(f"Current idle time: {format_time(current_idle_time)}.")

        if remaining_time <= 0:
            shutdown()
            break

        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main()
