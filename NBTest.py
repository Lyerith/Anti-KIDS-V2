import pandas as pd
import tkinter as tk
from tkinter import scrolledtext

# Function to compute the 'Analysis' column based on feature presence
def compute_analysis(row):
    if row['Keyboard Inputs'] or row['Programs Detected'] or row['Commands'] or row['Links']:
        return 'Malicious'
    else:
        return 'Not Malicious'

# Create the main tkinter window
root = tk.Tk()
root.title("Results")

# Create a scrolled text widget to display results
results_text = scrolledtext.ScrolledText(root, width=50, height=20)
results_text.pack()

# Load the dataset into a DataFrame
data = pd.read_csv("C:\\Users\\63929\\Desktop\\Anti-KIDS\\V1\\scan_results.csv")

# Get the most recent row (last row) from the DataFrame
latest_row = data.iloc[-1]

# Compute the 'Analysis' for the latest row
analysis_result = compute_analysis(latest_row)

# Display the result in the GUI
results_text.insert(tk.END, f"Latest USB Device: {latest_row['USB Device']}\n")
results_text.insert(tk.END, f"Analysis Result: {analysis_result}\n")
results_text.insert(tk.END, "-" * 20 + "\n")

# Start the tkinter main loop
root.mainloop()
