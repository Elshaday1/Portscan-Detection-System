import pyshark
import statistics


capture = pyshark.LiveCapture(interface='Ethernet')
is_capture_active = True

def calculate_mean_packet_length(interval):
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


# mean_length = calculate_mean_packet_length(20)
# std_dev = calculate_packet_length_std_dev(20)

# print("Mean Packet Length:", mean_length)
# print("Packet Length Standard Deviation:", std_dev)

while True:
    mean_length = calculate_mean_packet_length(20)
    std_dev = calculate_packet_length_std_dev(20)
    print("Mean Packet Length:", mean_length)
    print("Packet Length Standard Deviation:", std_dev)
