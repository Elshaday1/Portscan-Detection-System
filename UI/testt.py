import tkinter as tk

def handle_navigation(event):
    # Get the clicked navigation link
    target = event.widget
    
    # Remove active state from all navigation links
    for link in navigation_links:
        link.config(relief=tk.RAISED)
    
    # Set active state for the clicked navigation link
    target.config(relief=tk.SUNKEN)
    
    # Display content based on the clicked navigation link
    content_label.config(text=target.cget("text"))

# Create the main window
window = tk.Tk()
window.title("Intrusion Detection System")

# Create the header
header_frame = tk.Frame(window, bg="#333")
header_frame.pack(fill=tk.X)

title_label = tk.Label(header_frame, text="Intrusion Detection System", fg="white", bg="#333", padx=10, pady=10)
title_label.pack(side=tk.LEFT)

# Create the navigation bar
navigation_frame = tk.Frame(window)
navigation_frame.pack(side=tk.LEFT, fill=tk.Y)

navigation_links = []
navigation_options = ["Dashboard", "Packet Visualization", "Real-time Monitoring", "Configuration"]

for option in navigation_options:
    link = tk.Button(navigation_frame, text=option, relief=tk.RAISED, padx=10, pady=10)
    link.pack(fill=tk.X)
    link.bind("<Button-1>", handle_navigation)
    navigation_links.append(link)

# Create the content area
content_frame = tk.Frame(window, padx=10, pady=10)
content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

content_label = tk.Label(content_frame, text="Dashboard", font=("Arial", 18))
content_label.pack()

# Start the main loop
window.mainloop()
