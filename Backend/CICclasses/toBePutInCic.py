from enum import Enum
from typing import Any
# from decimal import Decimal

# from .import constants
import packet_flow_key
from packet_direction import PacketDirection
from flag_count import FlagCount
from flow_bytes import FlowBytes
from packet_count import PacketCount
from packet_length import PacketLength
from packet_time import PacketTime
from utils import get_statistics


class Flow:
    """This class summarizes the values of the features of the network flows"""

    def __init__(self, packet: Any, direction: Enum):
        """This method initializes an object from the Flow class.

        Args:
            packet (Any): A packet from the network.
            direction (Enum): The direction the packet is going ove the wire.
        """

        (
            self.dest_ip,
            self.src_ip,
            self.src_port,
            self.dest_port,
        ) = packet_flow_key.get_packet_flow_key(packet, direction)

        self.packets = []
        self.flow_interarrival_time = []
        self.latest_timestamp = 0
        self.start_timestamp = 0
        self.init_window_size = {
            PacketDirection.FORWARD: 0,
            PacketDirection.REVERSE: 0,
        }

        self.start_active = 0
        self.last_active = 0
        self.active = []
        self.idle = []

        self.forward_bulk_last_timestamp = 0
        self.forward_bulk_start_tmp = 0
        self.forward_bulk_count = 0
        self.forward_bulk_count_tmp = 0
        self.forward_bulk_duration = 0
        self.forward_bulk_packet_count = 0
        self.forward_bulk_size = 0
        self.forward_bulk_size_tmp = 0
        self.backward_bulk_last_timestamp = 0
        self.backward_bulk_start_tmp = 0
        self.backward_bulk_count = 0
        self.backward_bulk_count_tmp = 0
        self.backward_bulk_duration = 0
        self.backward_bulk_packet_count = 0
        self.backward_bulk_size = 0
        self.backward_bulk_size_tmp = 0



def get_data(self) -> dict:
    flow_bytes = FlowBytes(self)
    flag_count = FlagCount(self)
    packet_count = PacketCount(self)
    packet_length = PacketLength(self)
    packet_time = PacketTime(self)
    flow_iat = get_statistics(self.flow_interarrival_time)
    forward_iat = get_statistics(
    packet_time.get_packet_iat(PacketDirection.FORWARD)
        )
    backward_iat = get_statistics(
            packet_time.get_packet_iat(PacketDirection.REVERSE)
        )
    active_stat = get_statistics(self.active)
    idle_stat = get_statistics(self.idle)

    totalLength =  packet_length.get_total(PacketDirection.FORWARD)
    print(totalLength)

    

# "Packet Length Mean" : "pkt_len_mean": float(packet_length.get_mean()),
# "Flow Bytes/s" : "flow_byts_s": flow_bytes.get_rate(),
# "ACK Flag Count" : "ack_flag_cnt": flag_count.has_flag("ACK"),
# "Min Packet Length" : "pkt_len_min": packet_length.get_min(),
# "Destination Port" : "dst_port": self.dest_port,
# "Fwd IAT Min" : "flow_iat_min": float(flow_iat["min"]),
# "Bwd Packets/s" : "bwd_pkts_s": packet_count.get_rate(PacketDirection.REVERSE),
# "Bwd Packet Length Std" : "bwd_pkt_len_std": float(packet_length.get_std(PacketDirection.REVERSE)),
# "Init_Win_bytes_forward" : "init_fwd_win_byts": self.init_window_size[PacketDirection.FORWARD],
# "Bwd IAT Min" : "bwd_iat_min": float(backward_iat["min"]),
# "Init_Win_bytes_backward" : "init_bwd_win_byts": self.init_window_size[PacketDirection.REVERSE],
# "Idle Min" : "idle_min": float(idle_stat["min"]),
# "Total Length of Bwd Packets" : "totlen_bwd_pkts": packet_length.get_total(PacketDirection.REVERSE),
# "Flow Duration" : "flow_duration": 1e6 * packet_time.get_duration(),
# "Flow IAT Min" : "flow_iat_min": float(flow_iat["min"]),
# "Bwd Packet Length Mean" : "bwd_pkt_len_mean": float(packet_length.get_mean(PacketDirection.REVERSE)),
# "Packet Length Std" : "pkt_len_std": float(packet_length.get_std()),
# "Bwd Header Length" : "bwd_header_len": flow_bytes.get_reverse_header_bytes(),
# "Flow IAT Max" : "flow_iat_max": float(flow_iat["max"]),
# "min_seg_size_forward" : "fwd_seg_size_min": flow_bytes.get_min_forward_header_bytes(),
# "Flow IAT Mean" : "flow_iat_mean": float(flow_iat["mean"]),
# "Fwd Packet Length Max" : "fwd_pkt_len_max": float(packet_length.get_max(PacketDirection.FORWARD)),
# "Fwd IAT Mean" : "flow_iat_mean": float(flow_iat["mean"]),
# "Flow Packets/s" : "flow_pkts_s": packet_count.get_rate(),
# "Fwd Header Length" : "fwd_header_len": flow_bytes.get_forward_header_bytes()


