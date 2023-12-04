import os
import sys
import time
from dateutil import parser

def get_idle_time():
    # This function needs to be implemented based on the operating system.
    # For Windows, you can use ctypes to call the GetLastInputInfo from User32.dll
    # For Linux and MacOS, different methods will be required.
    pass

def shutdown():
    os.system("shutdown /s /f /t 0")  # Force shutdown command for Windows
    # For Linux, use 'shutdown now -h'
    # For MacOS, use 'shutdown -h now'

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

    print(f"System will shutdown after {input_time} of idle time.")
    while True:
        idle_time = get_idle_time()
        if idle_time >= wait_time:
            shutdown()
            break
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
