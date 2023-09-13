from scapy.all import *
from scapy.layers.inet import IP,TCP
from cicflowmeter import *

def process_packet(packet):
    # Extract relevant information from the packet
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    src_port = packet[TCP].sport
    dst_port = packet[TCP].dport
    protocol = packet[IP].proto

    # Create a flow object with the extracted information
    flow = Flow(src_ip, dst_ip, src_port, dst_port, protocol)

    # Perform flow analysis
    flow_analysis = FlowAnalysis()
    flow_analysis.compute_features(flow)

    # Get the specific features you want
    features = [
        'Total Length of Fwd Packets',
        'Packet Length Mean',
        'Flow Bytes/s',
        'ACK Flag Count',
        'Min Packet Length',
        'Destination Port',
        'Fwd IAT Min',
        'Bwd Packets/s',
        'Bwd Packet Length Std',
        'Init_Win_bytes_forward',
        'Bwd IAT Min',
        'Init_Win_bytes_backward',
        'Idle Min',
        'Total Length of Bwd Packets',
        'Flow Duration',
        'Flow IAT Min',
        'Bwd Packet Length Mean',
        'Packet Length Std',
        'Bwd Header Length',
        'Flow IAT Max',
        'min_seg_size_forward',
        'Flow IAT Mean',
        'Fwd Packet Length Max',
        'Fwd IAT Mean',
        'Flow Packets/s',
        'Fwd Header Length'
    ]

    # Print the analysis results for the specific features
    for feature in features:
        print(feature + ": " + str(flow_analysis.get_feature(feature)))

# Set the network interface to capture traffic from
iface = "eth0"  # Replace with the appropriate interface name

# Start capturing packets and process them in real-time
sniff(prn=process_packet)
