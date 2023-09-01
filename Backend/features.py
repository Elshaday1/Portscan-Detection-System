import pyshark
import math
import statistics
from datetime import datetime


def start_live_capture(interface='eth0', timeout=10):
    return pyshark.LiveCapture(interface=interface, display_filter='tcp', only_summaries=True, timeout=timeout)

# Get the destination ports from live capture
def get_destination_port_live_capture(interface):
    capture = pyshark.LiveCapture(interface=interface)
    destination_ports = []

    for packet in capture.sniff_continuously(packet_count=100):
        if 'tcp' in packet:
            destination_port = packet.tcp.dstport
            destination_ports.append(destination_port)
        elif 'udp' in packet:
            destination_port = packet.udp.dstport
            destination_ports.append(destination_port)

    return destination_ports

# Get the flow duration from the captured packets
def get_flow_duration(capture):
    if capture:
        start_time = datetime.fromisoformat(capture[0].time.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(capture[-1].time.replace('Z', '+00:00'))
        flow_duration = end_time - start_time
        return flow_duration

    return None

# Check if a specific flag is set in the packet
def check_flag(packet, flag_name):
    if flag_name in packet.tcp.flags:
        return 1
    else:
        return 0

# Calculate the flow IAT (Inter-Arrival Time) from a packet
def calculate_flow_iat(packet, capture_start_time):
    current_timestamp = datetime.strptime(packet.sniff_time, '%Y-%m-%d %H:%M:%S.%f')
    flow_iat = (current_timestamp - capture_start_time).total_seconds()
    return flow_iat

# Calculate the forward IAT (Inter-Arrival Time) from a packet
def calculate_forward_iat(packet, previous_timestamp):
    current_timestamp = datetime.fromisoformat(packet.frame_info.time.replace('Z', '+00:00'))
    forward_iat = (current_timestamp - previous_timestamp).total_seconds()
    return forward_iat, current_timestamp

# Calculate the backward IAT (Inter-Arrival Time) from a packet
def calculate_backward_iat(packet, response_timestamp):
    current_timestamp = datetime.fromisoformat(packet.frame_info.time.replace('Z', '+00:00'))
    backward_iat = (current_timestamp - response_timestamp).total_seconds()
    return backward_iat

# Extract forward packets from a list of packets
def extract_forward_packets(packets):
    forward_packets = []
    for packet in packets:
        if 'forward' in packet.layers:
            forward_packets.append(packet)
    return forward_packets

# Extract backward packets from a list of packets
def extract_backward_packets(packets):
    backward_packets = []
    for packet in packets:
        if 'backward' in packet.layers:
            backward_packets.append(packet)
    return backward_packets

# Calculate the total number of packets
def calculate_total_packets(packets):
    return len(packets)

# Calculate the total length of packets
def calculate_total_length(packets):
    total_length = 0
    for packet in packets:
        total_length += int(packet.length)
    return total_length

# Calculate the maximum and minimum length of packets
def calculate_max_min_length(packets):
    max_length = 0
    min_length = float('inf')
    for packet in packets:
        length = int(packet.length)
        if length > max_length:
            max_length = length
        if length < min_length:
            min_length = length
    return max_length, min_length

# Calculate the mean length of packets
def calculate_mean_length(packets):
    total_length = calculate_total_length(packets)
    total_packets = calculate_total_packets(packets)
    mean_length = total_length / total_packets
    return mean_length

# Calculate the standard deviation of packet lengths
def calculate_std_deviation(packets):
    mean_length = calculate_mean_length(packets)
    squared_diff_sum = 0
    for packet in packets:
        length = int(packet.length)
        squared_diff_sum += (length - mean_length) ** 2
    variance = squared_diff_sum / calculate_total_packets(packets)
    std_deviation = math.sqrt(variance)
    return std_deviation

# Extract packet length from a packet
packet_lengths = []
def extract_packet_length(packet):
    packet_length = int(packet.length)
    packet_lengths.append(packet_length)
    return packet_length

# Calculate the minimum length of packets
def calculate_min_length():
    return min(packet_lengths)

# Calculate the maximum length of packets
def calculate_max_length():
    return max(packet_lengths)

# Calculate the mean length of packets
def calculate_mean_length():
    return statistics.mean(packet_lengths)

# Calculate the standard deviation of packet lengths
def calculate_std_length():
    return statistics.stdev(packet_lengths)

# Calculate the variance of packet lengths
def calculate_variance_length():
    return statistics.variance(packet_lengths)

# Example usage
# cap = pyshark.FileCapture('your_packet_file.pcap')
# packets = list(cap)

forward_packets = extract_forward_packets(packets)
backward_packets = extract_backward_packets(packets)

total_forward_packets = calculate_total_packets(forward_packets)
total_backward_packets = calculate_total_packets(backward_packets)

total_forward_length = calculate_total_length(forward_packets)
total_backward_length = calculate_total_length(backward_packets)

max_forward_length, min_forward_length = calculate_max_min_length(forward_packets)
max_backward_length, min_backward_length = calculate_max_min_length(backward_packets)

mean_forward_length = calculate_mean_length(forward_packets)
mean_backward_length = calculate_mean_length(backward_packets)

std_deviation_forward = calculate_std_deviation(forward_packets)
std_deviation_backward = calculate_std_deviation(backward_packets)

# Example usage
previous_timestamp = None
response_timestamp = None

for packet in capture:
    current_timestamp = datetime.fromisoformat(packet.frame_info.time.replace('Z', '+00:00'))

    if previous_timestamp:
        forward_iat, previous_timestamp = calculate_forward_iat(packet, previous_timestamp)
        print(f"Forward IAT: {forward_iat}")
    else:
        previous_timestamp = current_timestamp

    if hasattr(packet, 'response_to'):
        if response_timestamp:
            backward_iat = calculate_backward_iat(packet, response_timestamp)
            print(f"Backward IAT: {backward_iat}")
        else:
            response_timestamp = current_timestamp

# Usage example
capture = start_live_capture()

# Perform feature extraction using the captured packets
if capture:
    start_time = datetime.fromisoformat(capture[0].time.replace('Z', '+00:00'))

    # Get flow duration
    flow_duration = get_flow_duration(capture)
    if flow_duration:
        print(f"Flow duration: {flow_duration}")

    previous_timestamp = None
    response_timestamp = None

    for packet in capture:
        # Check forward and backward flags
        forward_psh_flag = check_flag(packet, 'PSH')
        backward_psh_flag = check_flag(packet, 'PSH')
        forward_urg_flag = check_flag(packet, 'URG')
        backward_urg_flag = check_flag(packet, 'URG')

        # Calculate flow IAT
        flow_iat = calculate_flow_iat(packet, start_time)

        # Calculate forward IAT
        if previous_timestamp:
            forward_iat = calculate_forward_iat(packet, previous_timestamp)
        else:
            forward_iat = None

        # Calculate backward IAT
        if response_timestamp:
            backward_iat = calculate_backward_iat(packet, response_timestamp)
        else:
            backward_iat = None

        # Update previous timestamp and response timestamp
        previous_timestamp = datetime.strptime(packet.sniff_time, '%Y-%m-%d %H:%M:%S.%f')
        response_timestamp = datetime.strptime(packet.response_to, '%Y-%m-%d %H:%M:%S.%f')

        # Print or store the extracted features as needed
        print(f"Forward PSH flag: {forward_psh_flag}")
        print(f"Backward PSH flag: {backward_psh_flag}")
        print(f"Forward URG flag: {forward_urg_flag}")
        print(f"Backward URG flag: {backward_urg_flag}")
