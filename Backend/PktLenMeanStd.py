import pyshark
import statistics

capture = pyshark.LiveCapture(interface='Ethernet')
is_capture_active = True

def calculate_backward_packet_size(interval):
    backward_packet_sizes = []

    for packet in capture:
        if 'ack' in packet:
            backward_packet_sizes.append(int(packet.length))

        if len(backward_packet_sizes) == interval:
            backward_size = sum(backward_packet_sizes)
            backward_packet_sizes = []
            return backward_size

        if not is_capture_active:
            break

    return sum(backward_packet_sizes)

backward_size = calculate_backward_packet_size(2)
print("Size of Packets in the Backward Direction:", backward_size)

while is_capture_active:
    backward_size = calculate_backward_packet_size(2)
    print("Size of Packets in the Backward Direction:", backward_size)
