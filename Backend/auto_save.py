# import os
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler


# directory = 'C:\\Users\\Hp\\Desktop\\CIC'
# filename = 'packet.csv'
# file_path = os.path.join(directory, filename)
# backup_filename = 'Book1.csv'
# backup_file_path = os.path.join(directory, backup_filename)

# # Create a custom event handler to detect file modifications
# class FileModifiedHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         if event.src_path == file_path:
#             print(f"Detected changes in '{filename}'. Saving the new rows to '{backup_filename}'...")
#             save_new_rows()

# # Function to save the new rows to the backup file
# def save_new_rows():
#     global num_existing_rows
#     try:
#         # Read the new rows from the original file
#         with open(file_path, 'r') as file:
#             rows = file.readlines()

#         # Get the new rows starting from the last known position
#         new_rows = rows[num_existing_rows:]

#         # Append the new rows to the backup file
#         with open(backup_file_path, 'a') as backup_file:
#             backup_file.writelines(new_rows)

#         # Update the number of existing rows
#         num_existing_rows += len(new_rows)

#         print("New rows saved successfully to the backup file.")
#     except IOError:
#         print("An error occurred while saving the new rows.")

# # Create an observer and attach the event handler
# event_handler = FileModifiedHandler()
# observer = Observer()
# observer.schedule(event_handler, path=directory, recursive=False)
# observer.start()

# # Read the existing rows from the backup file
# with open(backup_file_path, 'r') as backup_file:
#     existing_rows = backup_file.readlines()
#     num_existing_rows = len(existing_rows)

# try:
#     while True:
#         # Read the new rows from the original file
#         with open(file_path, 'r') as file:
#             rows = file.readlines()

#         # Check if there are new rows to save
#         if len(rows) > num_existing_rows:
#             # Get the new rows starting from the last known position
#             new_rows = rows[num_existing_rows:]

#             # Append the new rows to the backup file
#             with open(backup_file_path, 'a') as backup_file:
#                 backup_file.writelines(new_rows)

#             # Update the number of existing rows
#             num_existing_rows += len(new_rows)

#             print("New rows saved successfully to the backup file.")

#         time.sleep(1)
# except KeyboardInterrupt:
#     observer.stop()

# observer.join()
import csv
import shutil

def backup_csv_file(source_file, backup_file):
    # Read the new rows from the source CSV file
    with open(source_file, 'r', newline='') as source_csv:
        reader = csv.reader(source_csv)
        new_rows = list(reader)  # Read all rows

    # Append the new rows to the backup CSV file
    with open(backup_file, 'a', newline='') as backup_csv:
        writer = csv.writer(backup_csv)
        writer.writerows(new_rows)

    print(f"New rows from '{source_file}' appended to '{backup_file}'.")

# Specify the source and backup file paths
source_file_path = 'C:\\Users\\Hp\\Desktop\\CIC\\packet.csv'
backup_file_path = 'C:\\Users\\Hp\\Desktop\\CIC\\backup.csv'

# Call the backup_csv_file function with the file paths
backup_csv_file(source_file_path, backup_file_path)