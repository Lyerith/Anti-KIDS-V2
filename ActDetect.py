import time
import pyautogui
import os
import threading
from pynput import keyboard
import sys
from datetime import datetime  # Import datetime module to get the current date and time

# Define the list of target window titles to close
TARGET_WINDOW_TITLES = ["Run", "Windows PowerShell", "Command Prompt"]

# Define the inactivity threshold in seconds
INACTIVITY_THRESHOLD = 10

# Initialize global variables
last_key_press_time = time.time()
inactivity_timer = threading.Timer(INACTIVITY_THRESHOLD, None)
inactivity_timer.start()
closed_windows_during_inactivity = []  # List to track closed windows during inactivity
closed_windows_during_scan = []  # List to track closed windows during inactivity

def block_common_keys():
    import keyboard
    # List of common keys and symbols to block
    common_keys = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
        "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "space", "enter", "tab", "backspace", "esc", "ctrl", "alt",
        "left", "right", "up", "down", "home", "end", "insert", "delete",
        "page up", "page down", "caps lock", "num lock", "scroll lock",
        "print screen", "menu", "windows", "cmd",
        "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
        "`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/",  # Add more symbols as needed
    ]

    # Block all common keys and symbols
    for key in common_keys:
        keyboard.block_key(key)

def detect_and_close_windows():
    closed_windows = []
    for window_title in TARGET_WINDOW_TITLES:
        if detect_window(window_title):
            closed_windows.append(window_title)
            close_window(window_title)
    closed_windows_during_scan.extend(closed_windows)  # Append closed windows to the list
    return closed_windows

def detect_window(window_title):
    windows = pyautogui.getWindowsWithTitle(window_title)
    return len(windows) > 0

def close_window(window_title):
    global closed_windows_during_inactivity
    windows = pyautogui.getWindowsWithTitle(window_title)
    for window in windows:
        window.close()
    closed_windows_during_inactivity.append(window_title)  # Add closed window to the list

def log_window_closed(window_title=None):
    with open(output_file, "a") as logKey:
        if window_title is not None:
            logKey.write(f"Window '{window_title}' closed\n")

def log_keystroke(key_str):
    with open(output_file, "a") as logKey:
        logKey.write(key_str)

def key_pressed(key):
    global last_key_press_time
    global inactivity_timer
    global total_words
    global start_time

    # Skip recording Shift key
    if key == keyboard.Key.shift:
        return

    last_key_press_time = time.time()
    # Reset the inactivity timer when a key is pressed
    inactivity_timer.cancel()
    inactivity_timer = threading.Timer(INACTIVITY_THRESHOLD, None)
    inactivity_timer.start()

    try:
        key_str = ""
        if key == keyboard.Key.space:
            key_str = " "
        elif key == keyboard.Key.enter:
            key_str = "\n"
        elif hasattr(key, 'char'):
            key_str = key.char
            total_words += 1
        else:
            special_key = None
            if hasattr(key, 'vk'):
                special_key = key.vk
            elif hasattr(key, 'name'):
                special_key = key.name
            if special_key is not None:
                if isinstance(key, keyboard.Key):
                    key_str = f" <{key.name}> "
                else:
                    key_str = f" <{special_key}> "

        if key_str:
            log_keystroke(key_str)

    except Exception as e:
        print(f"Error: {e}")

    start_time = time.time()

def calculate_wpm(total_words, elapsed_time):
    words_per_minute = (total_words / 5) / (elapsed_time / 60)
    return words_per_minute

def save_wpm(wpm, file_path):
    with open(file_path, "a") as logKey:
        logKey.write(f"\n WPM: {wpm:.2f}\n")

def reset_inactivity_timer():
    global inactivity_timer
    inactivity_timer.cancel()
    inactivity_timer = threading.Timer(INACTIVITY_THRESHOLD, reset_inactivity_timer)
    inactivity_timer.start()

def inactivity_checker():
    global closed_windows_during_inactivity
    while True:
        current_time = time.time()
        if current_time - last_key_press_time > INACTIVITY_THRESHOLD:
            listener.stop()
            wpm = calculate_wpm(total_words, current_time - start_time)
            print(f"Final WPM: {wpm:.2f}")
            save_wpm(wpm, output_file)
            print("Exiting program due to inactivity.")
            save_closed_windows(closed_windows_during_inactivity, output_file)
            if closed_windows_during_scan:
                print("Windows closed during scan:")
                for window_title in closed_windows_during_scan:
                    print(f"- {window_title}")
            os._exit(0)  # Terminate the program

        time.sleep(1)

def save_closed_windows(closed_windows, file_path):
    with open(file_path, "a") as file:
        file.write("\nWindows closed during scan:\n")
        for window_title in closed_windows:
            file.write(f"{window_title}\n")

if __name__ == "__main__":
    block_common_keys()

    # Specify the output directory here
    output_directory = "C:\\Users\\63929\\Desktop\\Anti-KIDS\\V1\\logs"
    
    # Get the current date and time as a string
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Specify the output file path here, including the device name and date and time
    device_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown_Device"
    output_file = os.path.join(output_directory, f"{device_name}_{current_datetime}.txt")

    start_time = time.time()
    total_words = 0

    # Start the inactivity checker thread
    inactivity_thread = threading.Thread(target=inactivity_checker)
    inactivity_thread.daemon = True
    inactivity_thread.start()

    # Start the key listener
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()

    # Initialize the inactivity timer with the reset_inactivity_timer function
    inactivity_timer = threading.Timer(INACTIVITY_THRESHOLD, reset_inactivity_timer)
    inactivity_timer.start()

    while True:
        closed_windows = detect_and_close_windows()  # Check for and close windows
        time.sleep(1)
