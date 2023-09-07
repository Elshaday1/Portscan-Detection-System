import pyshark
import statistics

#capture = pyshark.LiveCapture(interface='Ethernet')
interface_type = "Ethernet"
if interface_type == "Ethernet":
    capture = pyshark.LiveCapture(interface='Ethernet')
elif interface_type == "Wifi":
    capture = pyshark.LiveCapture(interface='Wifi')
else:
    print("NOT CONNECTED TO A VALID INTERFACE")


def calculate_packet_length_mean(interval):
    packet_count = 0
    total_length = 0

    for packet in capture:
        packet_count += 1
        total_length += int(packet.length)

        if packet_count % interval == 0:
            mean_length = total_length / interval
            total_length = 0
            return mean_length


def calculate_packet_length_std_dev(interval):
    packet_lengths = []

    for packet in capture:
        packet_lengths.append(int(packet.length))

        if len(packet_lengths) == interval:
            std_dev = statistics.stdev(packet_lengths)
            packet_lengths = []
            return std_dev

def calculate_min_packet_length(interval):
    packet_count = 0
    min_length = float('inf')

    for packet in capture:
        packet_count += 1
        packet_length = int(packet.length)

        if packet_length < min_length:
            min_length = packet_length

        if packet_count % interval == 0:
            return min_length
            min_length = float('inf')

    return min_length

# def calculate_backward_packet_length_mean(interval):
#     backward_packet_lengths = []

#     for packet in capture:
#         if 'ack' in packet:
#             backward_packet_lengths.append(int(packet.length))

#         if len(backward_packet_lengths) == interval:
#             mean_length = statistics.mean(backward_packet_lengths)
#             backward_packet_lengths = []
#             return mean_length

#     return statistics.mean(backward_packet_lengths)

# def calculate_backward_packet_length_std_dev(interval):
#     backward_packet_lengths = []

#     for packet in capture:
#         if 'ack' in packet:
#             backward_packet_lengths.append(int(packet.length))

#         if len(backward_packet_lengths) == interval:
#             std_dev = statistics.stdev(backward_packet_lengths)
#             backward_packet_lengths = []
#             return std_dev

#     return statistics.stdev(backward_packet_lengths)

capture.sniff_continuously()

#dictionary to store the feature values
features = {}

for packet in capture:
    # Extract the desired features from the packet
    if 'tcp' in packet:
        features['Total Length of Fwd Packets'] = packet.tcp.len
        features['Packet Length Mean'] = calculate_packet_length_mean(20)
        features['ACK Flag Count'] = packet.tcp.flags_ack
        features['Min Packet Length'] = calculate_min_packet_length(20)
        features['Destination Port'] = packet.tcp.dstport
       # features['Fwd IAT Min'] = IAT_Values['Fwd IAT Min'] #packet.tcp.sniff_time
        features['Bwd Packet Length Std'] = packet.length
        features['Init_Win_bytes_forward'] = packet.tcp.window_size
        #features['Bwd IAT Min'] = packet.tcp.sniff_time
        features['Init_Win_bytes_backward'] = packet.tcp.window_size
        features['Total Length of Bwd Packets'] = packet.tcp.len
        #features['Flow IAT Min'] = packet.sniff_time
        features['Bwd Packet Length Mean'] = packet.length
        features['Packet Length Std'] = calculate_packet_length_std_dev(20)
        features['Bwd Header Length'] = packet.length
        #features['Flow IAT Max'] = packet.sniff_time
        features['min_seg_size_forward'] = packet.length
        #features['Flow IAT Mean'] = packet.sniff_time
        features['Fwd Packet Length Max'] = packet.length
        #features['Fwd IAT Mean'] = packet.sniff_time
        features['Fwd Header Length'] = packet.length

    #extracted features printed in a loop
    for feature, value in features.items():
        print(f"{feature}: {value}")
