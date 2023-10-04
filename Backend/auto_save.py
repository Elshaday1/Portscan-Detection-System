# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from pynput import keyboard

# # Define the directory and file to monitor
# directory = 'C:\\Users\\Hp\Desktop\\CIC'
# filename = 'packet.csv'
# file_path = os.path.join(directory, filename)
# backup_filename = 'backup.csv'
# backup_file_path = os.path.join(directory, backup_filename)

# # Create a custom event handler to detect file modifications
# class FileModifiedHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         if event.src_path == file_path:
#             print(f"Detected changes in '{filename}'. Saving the new rows to '{backup_filename}'...")
#             save_new_rows()

# # Function to save the new rows to the backup file
# def save_new_rows():
#     try:
#         # Read the new rows from the original file
#         with open(file_path, 'r') as file:
#             rows = file.readlines()

#         # Append the new rows to the backup file
#         with open(backup_file_path, 'a') as backup_file:
#             new_rows = rows[len(existing_rows):]  # Only append the new rows
#             backup_file.writelines(new_rows)

#         print("New rows saved successfully to the backup file.")
#     except IOError:
#         print("An error occurred while saving the new rows.")

# # Function to handle keyboard input
# def on_press(key):
#     if key == keyboard.Key.enter:
#         save_new_rows()

# # Create an observer and attach the event handler
# event_handler = FileModifiedHandler()
# observer = Observer()
# observer.schedule(event_handler, path=directory, recursive=False)
# observer.start()

# # Read the existing rows from the backup file
# with open(backup_file_path, 'r') as backup_file:
#     existing_rows = backup_file.readlines()

# # Start monitoring the keyboard input
# listener = keyboard.Listener(on_press=on_press)
# listener.start()

# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     observer.stop()

# observer.join()
# listener.stop()
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pynput import keyboard


directory = 'C:\\Users\\Hp\Desktop\\CIC'
filename = 'packet.csv'
file_path = os.path.join(directory, filename)
backup_filename = 'Book1.csv'
backup_file_path = os.path.join(directory, backup_filename)

# Create a custom event handler to detect file modifications
class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == file_path:
            print(f"Detected changes in '{filename}'. Saving the new rows to '{backup_filename}'...")
            save_new_rows()

# Function to save the new rows to the backup file
def save_new_rows():
    try:
        # Read the new rows from the original file
        with open(file_path, 'r') as file:
            rows = file.readlines()
        
        # Check if there are new rows to save
        if len(rows) > num_existing_rows:
            new_rows = rows[num_existing_rows:]  # Get the new rows

            # Append the new rows to the backup file
            with open(backup_file_path, 'a') as backup_file:
                backup_file.writelines(new_rows)

            print("New rows saved successfully to the backup file.")
        else:
            print("No new rows to save.")
    except IOError:
        print("An error occurred while saving the new rows.")

# Function to handle keyboard input
def on_press(key):
    if key == keyboard.Key.enter:
        save_new_rows()

# Create an observer and attach the event handler
event_handler = FileModifiedHandler()
observer = Observer()
observer.schedule(event_handler, path=directory, recursive=False)
observer.start()

# Read the existing rows from the backup file
with open(backup_file_path, 'r') as backup_file:
    existing_rows = backup_file.readlines()
    num_existing_rows = len(existing_rows)

# Start monitoring the keyboard input
listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
listener.stop()