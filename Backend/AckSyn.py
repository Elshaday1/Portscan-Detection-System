from scapy.all import *

total_connections = 0
flagged_connections = 0

def packet_handler(packet):
    global total_connections, flagged_connections

    # Check if the packet is an Ethernet packet
    if Ether in packet:
        total_connections += 1

        # Extract relevant fields from the Ethernet packet
        dst_host_count = packet[IP].dst
        flag = packet[TCP].flags

        # Check the desired criteria for flagged connections
        if dst_host_count == 32 and flag in ['S0', 'S1', 'S2', 'S3']:
            flagged_connections += 1

# Start capturing Ethernet packets on your local network
sniff(filter="ether proto \ip", prn=packet_handler)

percentage = (flagged_connections / total_connections) * 100
print(f"The percentage of connections with activated flag among dst_host_count is: {percentage}%")
