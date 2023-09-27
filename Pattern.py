import re
import os
import time
import csv
import subprocess

def scan_for_keyboard_inputs(text):
    keyboard_inputs = []
    
    # Define a regular expression pattern to match keyboard input events
    pattern = r'<kbd>[^\n]*</kbd>'
    
    # Find all matches in the input text using the pattern
    matches = re.findall(pattern, text)
    
    # Append the matches to the result list
    keyboard_inputs.extend(matches)
    
    return keyboard_inputs

def scan_for_start_key_combinations(text):
    start_key_combinations = []
    # Define a regular expression pattern to match the desired format
    pattern = r'<cmd> [a-zA-Z]'
    # Find all matches in the input text using the pattern
    matches = re.findall(pattern, text)
    # Append the matches to the result list
    start_key_combinations.extend(matches)
    return start_key_combinations

def scan_for_windows_programs(text):
    windows_programs = []
    program_keywords = ["powershell", "command prompt", "run"]
    
    for keyword in program_keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            windows_programs.append(match)

    return windows_programs

def scan_for_links(text):
    links = []
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\\\(\\\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    matches = re.findall(pattern, text)
    for match in matches:
        links.append(match)
    return links

def scan_for_powershell_commands(text):
    powershell_commands = []
    lines = text.split('\n')
    for line in lines:
        # Check if the line contains a valid PowerShell command symbol or operator
        if any(symbol in line for symbol in ['|', '=', '$', '.', ';', '&', ':', '"', "'", '`', '-']):
            # Exclude lines containing "WPM:" or "Windows closed during scan:"
            if "WPM:" not in line and "Windows closed during scan:" not in line:
                # Check if the line contains "http" or "https" (a common indicator of links)
                if "http" not in line and "https" not in line:
                    powershell_commands.append(line.strip())

    return powershell_commands

def scan_recent_text_files_in_directory(directory):
    # Get the current time
    current_time = time.time()
    # Define a threshold for recent files (e.g., files created within the last 24 hours)
    recent_threshold = 24 * 60 * 60  # 24 hours in seconds
    # Create a list to store the paths of recent text files
    recent_text_files = []
    # Iterate over files in the specified directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Get the creation time of the file
            file_creation_time = os.path.getctime(file_path)
            
            # Check if the file was created recently
            if current_time - file_creation_time <= recent_threshold:
                recent_text_files.append(file_path)
    
    return recent_text_files

def scan_most_recent_text_file_in_directory(directory):
    # Get the current time
    current_time = time.time()
    
    # Define a threshold for recent files (e.g., files created within the last 24 hours)
    recent_threshold = 24 * 60 * 60  # 24 hours in seconds
    
    # Initialize variables to track the most recent file and its creation time
    most_recent_file = None
    most_recent_creation_time = 0
    
    # Define the allowed file extensions for text files
    text_file_extensions = ['.txt', '.log', '.md', '.csv']  # Add more extensions as needed
    
    # Iterate over files in the specified directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Check if the file has a valid text file extension
            if any(file_path.lower().endswith(ext) for ext in text_file_extensions):
                # Get the creation time of the file
                file_creation_time = os.path.getctime(file_path)
                
                # Check if the file was created recently and is more recent than the current most recent file
                if current_time - file_creation_time <= recent_threshold and file_creation_time > most_recent_creation_time:
                    most_recent_file = file_path
                    most_recent_creation_time = file_creation_time
    
    return most_recent_file

def append_csv(filename, data):
    fieldnames = ['USB Device', 'Keyboard Inputs', 'Programs Detected', 'Commands', 'Links']  # Add 'Keyboard Inputs' column
    
    # Check if the file already exists
    file_exists = os.path.exists(filename)
    
    with open(filename, mode='a', newline='') as csv_file:  # Use 'a' (append) mode
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write the header row only if the file doesn't exist
        if not file_exists:
            writer.writeheader()
        
        # Determine whether to set values as 'True' or 'False' based on the presence of items
        programs_detected = len(windows_programs) > 0
        commands_detected = len(command_lines) > 0
        links_detected = len(links) > 0
        
        # Set 'Keyboard Inputs' to 'True' if there are commands or links detected, otherwise 'False'
        keyboard_inputs_detected = commands_detected or links_detected
        
        # Extract the file name from the full path
        data_filename = os.path.basename(data)
        
        # Write the data for the most recent file
        writer.writerow({
            'USB Device': data_filename,  # Use data_filename as the USB Device
            'Keyboard Inputs': keyboard_inputs_detected,  # Set 'Keyboard Inputs' based on commands or links
            'Programs Detected': programs_detected,
            'Commands': commands_detected,
            'Links': links_detected,
        })


def Bayes_file():
    subprocess.call(["python", "NBTest.py"])

if __name__ == "__main__":
    # Specify the directory where you want to search for recent text files
    search_directory = "C:\\Users\\63929\\Desktop\\Anti-KIDS\\V1\\logs"
    
    # Get the most recent text file in the specified directory
    most_recent_file = scan_most_recent_text_file_in_directory(search_directory)
    
    # Check if there is a most recently created text file
    if not most_recent_file:
        print("No recent text files found.")
    else:
        try:
            with open(most_recent_file, 'r') as file:
                input_text = file.read()
        except FileNotFoundError:
            print(f"File not found: {most_recent_file}")
        else:
            command_lines = scan_for_powershell_commands(input_text)
            start_key_combinations = scan_for_start_key_combinations(input_text)
            links = scan_for_links(input_text)
            windows_programs = scan_for_windows_programs(input_text)
            keyboard_inputs = scan_for_keyboard_inputs(input_text)  # Add keyboard input scanning
            
            # Extract the file name from the path
            most_recent_filename = os.path.basename(most_recent_file)
            
            # Output the results for the most recent file
            print(f"\nScanning most recently created file: {most_recent_filename}")  # Use most_recent_filenam
            
            start_key_count = len(start_key_combinations)
            command_count = len(command_lines)
            links_count = len(links)
            keyboard_inputs_count = len(keyboard_inputs)  # Count of detected keyboard inputs
            
            # Check if there are any scanned links or commands detected
            if links_count > 0 or command_count > 0:
                print("Keyboard input detected")
            elif windows_programs:
                print("Keyboard input detected")  # Add this condition to print for windows programs detected
            else:
                print("No Keyboard Inputs detected")

            if windows_programs:
                print("\nWindows Programs Detected:")
                for idx, program in enumerate(windows_programs, start=1):
                    print(f"{idx}. {program}")
            else:
                print("\nNo Windows Programs detected.")
            
            if command_lines:
                print("\nPossible Commands Detected:")
                for idx, line in enumerate(command_lines, start=1):
                    print(f"{idx}. {line}")
            else:
                print("\nNo Possible Commands detected.")

            if links:
                print("\nLinks Detected:")
                for idx, link in enumerate(links, start=1):
                    print(f"{idx}. {link}")
            else:
                print("\nNo Links detected.")

            print(f"\nCommands Detected: {command_count}")
            print(f"Links Detected: {links_count}\n")

            print("-" * 50)  # Separator for different files
            
            # Append the data to the CSV file
            csv_filename = "scan_results.csv"
            append_csv(csv_filename, most_recent_file)
            
            print(f"Data appended to CSV file '{csv_filename}'")
            