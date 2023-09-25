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

    "Total Length of Fwd Packets" :  packet_length.get_total(PacketDirection.FORWARD),
    "Packet Length Mean" : float(packet_length.get_mean()),
    "Flow Bytes/s" : flow_bytes.get_rate(),
    "ACK Flag Count"  : flag_count.has_flag("ACK"),
    "Min Packet Length" : packet_length.get_min(),
    "Destination Port" : self.dest_port,
    "Fwd IAT Min" :  float(flow_iat["min"]),
    "Bwd Packets/s" :  packet_count.get_rate(PacketDirection.REVERSE),
    "Bwd Packet Length Std" : float(packet_length.get_std(PacketDirection.REVERSE)),
    "Init_Win_bytes_forward" :  self.init_window_size[PacketDirection.FORWARD],
    "Bwd IAT Min" : float(backward_iat["min"]),
    "Init_Win_bytes_backward" :  self.init_window_size[PacketDirection.REVERSE],
    "Idle Min" :  float(idle_stat["min"]),
    "Total Length of Bwd Packets" : packet_length.get_total(PacketDirection.REVERSE),
    "Flow Duration" :  1e6 * packet_time.get_duration(),
    "Flow IAT Min" :  float(flow_iat["min"]),
    "Bwd Packet Length Mean" : float(packet_length.get_mean(PacketDirection.REVERSE)),
    "Packet Length Std" :  float(packet_length.get_std()),
    "Bwd Header Length" :  flow_bytes.get_reverse_header_bytes(),
    "Flow IAT Max" : float(flow_iat["max"]),
    "min_seg_size_forward" :  flow_bytes.get_min_forward_header_bytes(),
    "Flow IAT Mean" :  float(flow_iat["mean"]),
    "Fwd Packet Length Max" :  float(packet_length.get_max(PacketDirection.FORWARD)),
    "Fwd IAT Mean" :  float(flow_iat["mean"]),
    "Flow Packets/s" :  packet_count.get_rate(),
    "Fwd Header Length" : flow_bytes.get_forward_header_bytes()



