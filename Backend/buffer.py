# from scapy.all import *

# # Create an empty list to store the packets
# packet_buffer = []

# # Define a callback function to handle incoming packets
# def packet_handler(packet):
#     packet_buffer.append(packet)

# # Start capturing packets using the sniff() function
# sniff(prn=packet_handler)

# # You can specify additional parameters in the sniff() function to filter specific packets, such as 'filter', 'iface', or 'count'.

# # Perform some operations on the captured packets
# for packet in packet_buffer:
#     # Process each packet as per your requirements
#     print(packet.summary())
from scapy.all import *
import queue

# Create a packet buffer using a queue
packet_buffer = queue.Queue()

# Variable to track if packets should be buffered or not
allow_packets = False

# Function to handle received packets
def packet_handler(packet):
    global allow_packets

    if allow_packets:
        # Process the packet immediately
        process_packet(packet)
    else:
        # Buffer the packet
        packet_buffer.put(packet)

# Function to process a single packet
def process_packet(packet):
    # Process the packet as needed
    print("Processing packet:", packet.summary())

# Sniff packets and call packet_handler function for each packet received
sniff(filter="tcp", prn=packet_handler)  # Replace <your_filter> with any desired packet filter
