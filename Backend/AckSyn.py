from scapy.all import *
from scapy.layers.inet import IP, TCP

total_connections = 0
flagged_connections = 0

def packet_handler(packet):
    global total_connections, flagged_connections

    # Extract relevant fields from the packet
    if IP in packet and TCP in packet:
        dst_host_count = packet[IP].dst
        flag = packet[TCP].flags

        # Check the desired criteria for flagged connections
        if dst_host_count == 32 and flag in ['S0', 'S1', 'S2', 'S3']:
            flagged_connections += 1

    total_connections += 1

# Start capturing packets on your local network
sniff(filter="tcp", prn=packet_handler)

percentage = (flagged_connections / total_connections) * 100
print(f"The percentage of connections with activated flag among dst_host_count is: {percentage}%")
