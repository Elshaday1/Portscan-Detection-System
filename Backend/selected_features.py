import pyshark

#capture = pyshark.LiveCapture(interface='Ethernet')
interface_type = "Ethernet"
if interface_type == "Ethernet":
    capture = pyshark.LiveCapture(interface='Ethernet')
elif interface_type == "Wifi":
    capture = pyshark.LiveCapture(interface='Wifi')
else:
    print("Not connected to a valid interface")



def calculate_mean_packet_length(interval):
    packet_count = 0
    total_length = 0
    mean_length = 0

    for packet in capture:
        packet_count += 1
        total_length += int(packet.length)

        if packet_count % interval == 0:
            mean_length = total_length / interval
            total_length = 0
            return mean_length

    return mean_length

# Assume you already have the live capture object 'capture'

# Call the function to calculate the mean packet length every 20 packets
mean_length = calculate_mean_packet_length(20)

print("Mean Packet Length:", mean_length)






capture.sniff_continuously()

# def calculate_time_features():
#     # Initialize variables for the time features
#     fwd_iat_min = float('inf')
#     bwd_iat_min = float('inf')
#     flow_iat_min = float('inf')
#     flow_iat_max = float('-inf')
#     flow_iat_sum = 0
#     count = 0

#     for packet in capture:
#         if 'tcp' in packet:
#             #time related features
#             time_relative = float(packet.frame_info.time_relative)
#             flow_iat = time_relative - flow_iat_sum
#             flow_iat_sum += flow_iat

#             #minimum and maximum values
#             fwd_iat_min = min(fwd_iat_min, time_relative)
#             bwd_iat_min = min(bwd_iat_min, time_relative)
#             flow_iat_min = min(flow_iat_min, flow_iat)
#             flow_iat_max = max(flow_iat_max, flow_iat)

#             count += 1

#     #mean values
#     fwd_iat_mean = fwd_iat_min / count if count > 0 else 0
#     flow_iat_mean = flow_iat_sum / count if count > 0 else 0

#     return {
#         'Fwd IAT Min': fwd_iat_min,
#         'Bwd IAT Min': bwd_iat_min,
#         'Flow IAT Min': flow_iat_min,
#         'Flow IAT Max': flow_iat_max,
#         'Flow IAT Mean': flow_iat_mean,
#         'Fwd IAT Mean': fwd_iat_mean
#     }
#dictionary to store the feature values
features = {}
#IAT_Values = calculate_time_features()

# fwd_iat_min = IAT_Values['Fwd IAT Min']
# bwd_iat_min = IAT_Values['Bwd IAT Min']
# flow_iat_min = IAT_Values['Flow IAT Min']
# flow_iat_max = IAT_Values['Flow IAT Max']
# flow_iat_mean = IAT_Values['Flow IAT Mean']
# fwd_iat_mean = IAT_Values['Fwd IAT Mean']
# Iterate over the captured packets

for packet in capture:
    # Extract the desired features from the packet
    if 'tcp' in packet:
        features['Total Length of Fwd Packets'] = packet.tcp.len
        features['Packet Length Mean'] = packet.length
        features['ACK Flag Count'] = packet.tcp.flags_ack
        features['Min Packet Length'] = packet.length
        features['Destination Port'] = packet.tcp.dstport
       # features['Fwd IAT Min'] = IAT_Values['Fwd IAT Min'] #packet.tcp.sniff_time
        features['Bwd Packet Length Std'] = packet.length
        features['Init_Win_bytes_forward'] = packet.tcp.window_size
        #features['Bwd IAT Min'] = packet.tcp.sniff_time
        features['Init_Win_bytes_backward'] = packet.tcp.window_size
        features['Total Length of Bwd Packets'] = packet.tcp.len
        #features['Flow IAT Min'] = packet.sniff_time
        features['Bwd Packet Length Mean'] = packet.length
        features['Packet Length Std'] = packet.length
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
