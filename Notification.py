import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import time
import sys
import os

#temporary UI
def run_script():
    def simulate_script():
        try:
            # Replace 'your_script.py' with the actual Python script you want to run.
            subprocess.run(["python", "ActDetect.py", f"{device_name}"])
            progress_bar.stop()  # Stop the progress bar animation
            status_label.config(text="Script is done")
            root.quit()  # Close the window
        except Exception as e:
            progress_bar.stop()
            status_label.config(text=f"Error: {str(e)}")

    progress_bar.start(15)  # Start the progress bar animation
    status_label.config(text="All Keyboard Inputs Disabled...")
    
    # Simulate your Python script execution here.
    # You can replace this with your actual script.
    thread = threading.Thread(target=simulate_script)
    thread.start()

root = tk.Tk()
root.title("Anti-K.I.Ds Notification Window")

# Set the window size to 400x200
root.geometry("400x200")

device_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown_Device"

# Create a label to display the device name
device_label = ttk.Label(root, text=f"Device Name: {device_name}", font=("Helvetica", 12))
device_label.pack(pady=5)

notification_frame = ttk.Frame(root)
notification_frame.pack(padx=10, pady=10)

# Create a label to display a message above the loading bar
message_label = ttk.Label(notification_frame, text="Please Wait... Scanning in Progress", font=("Helvetica", 12))
message_label.pack(pady=5)

progress_bar = ttk.Progressbar(notification_frame, mode="determinate", length=200)
progress_bar.pack(pady=10)

status_label = ttk.Label(notification_frame, font=("Helvetica", 12))
status_label.pack(pady=5)

run_script()  # Automatically run the script when the window is created

root.mainloop()
