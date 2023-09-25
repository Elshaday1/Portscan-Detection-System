from enum import Enum
from typing import Any
# from decimal import Decimal

from .import constants
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

    data = {
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

    }

    def add_packet(self, packet: Any, direction: Enum) -> None:
        """Adds a packet to the current list of packets.

        Args:
            packet: Packet to be added to a flow
            direction: The direction the packet is going in that flow

        """
        self.packets.append((packet, direction))

        self.update_flow_bulk(packet, direction)
        self.update_subflow(packet)

        if self.start_timestamp != 0:
            self.flow_interarrival_time.append(
                float("1e6") * (packet.time - self.latest_timestamp)
            )

        self.latest_timestamp = max([packet.time, self.latest_timestamp])

        if "TCP" in packet:
            if (
                direction == PacketDirection.FORWARD
                and self.init_window_size[direction] == 0
            ):
                self.init_window_size[direction] = packet["TCP"].window
            elif direction == PacketDirection.REVERSE:
                self.init_window_size[direction] = packet["TCP"].window

        # First packet of the flow
        if self.start_timestamp == 0:
            self.start_timestamp = packet.time
            self.protocol = packet.proto

    def update_subflow(self, packet):
        """Update subflow

        Args:
            packet: Packet to be parse as subflow

        """
        last_timestamp = (
            self.latest_timestamp if self.latest_timestamp != 0 else packet.time
        )
        if (packet.time - (float(last_timestamp) / float("1e6"))) > constants.CLUMP_TIMEOUT:
            self.update_active_idle(packet.time - last_timestamp)

    def update_active_idle(self, current_time):
        """Adds a packet to the current list of packets.

        Args:
            packet: Packet to be update active time

        """
        if (current_time - self.last_active) > constants.ACTIVE_TIMEOUT:
            duration = abs(float(self.last_active - self.start_active))
            if duration > 0:
                self.active.append(1e6 * duration)
            self.idle.append(float("1e6") * (current_time - self.last_active))
            self.start_active = current_time
            self.last_active = current_time
        else:
            self.last_active = current_time

    def update_flow_bulk(self, packet, direction):
        """Update bulk flow

        Args:
            packet: Packet to be parse as bulk

        """
        payload_size = len(PacketCount.get_payload(packet))
        if payload_size == 0:
            return
        if direction == PacketDirection.FORWARD:
            if self.backward_bulk_last_timestamp > self.forward_bulk_start_tmp:
                self.forward_bulk_start_tmp = 0
            if self.forward_bulk_start_tmp == 0:
                self.forward_bulk_start_tmp = packet.time
                self.forward_bulk_last_timestamp = packet.time
                self.forward_bulk_count_tmp = 1
                self.forward_bulk_size_tmp = payload_size
            else:
                if (
                    packet.time - self.forward_bulk_last_timestamp
                ) > constants.CLUMP_TIMEOUT:
                    self.forward_bulk_start_tmp = packet.time
                    self.forward_bulk_last_timestamp = packet.time
                    self.forward_bulk_count_tmp = 1
                    self.forward_bulk_size_tmp = payload_size
                else:  # Add to bulk
                    self.forward_bulk_count_tmp += 1
                    self.forward_bulk_size_tmp += payload_size
                    if self.forward_bulk_count_tmp == constants.BULK_BOUND:
                        self.forward_bulk_count += 1
                        self.forward_bulk_packet_count += self.forward_bulk_count_tmp
                        self.forward_bulk_size += self.forward_bulk_size_tmp
                        self.forward_bulk_duration += (
                            packet.time - self.forward_bulk_start_tmp
                        )
                    elif self.forward_bulk_count_tmp > constants.BULK_BOUND:
                        self.forward_bulk_packet_count += 1
                        self.forward_bulk_size += payload_size
                        self.forward_bulk_duration += (
                            packet.time - self.forward_bulk_last_timestamp
                        )
                    self.forward_bulk_last_timestamp = packet.time
        else:
            if self.forward_bulk_last_timestamp > self.backward_bulk_start_tmp:
                self.backward_bulk_start_tmp = 0
            if self.backward_bulk_start_tmp == 0:
                self.backward_bulk_start_tmp = packet.time
                self.backward_bulk_last_timestamp = packet.time
                self.backward_bulk_count_tmp = 1
                self.backward_bulk_size_tmp = payload_size
            else:
                if (
                    packet.time - self.backward_bulk_last_timestamp
                ) > constants.CLUMP_TIMEOUT:
                    self.backward_bulk_start_tmp = packet.time
                    self.backward_bulk_last_timestamp = packet.time
                    self.backward_bulk_count_tmp = 1
                    self.backward_bulk_size_tmp = payload_size
                else:  # Add to bulk
                    self.backward_bulk_count_tmp += 1
                    self.backward_bulk_size_tmp += payload_size
                    if self.backward_bulk_count_tmp == constants.BULK_BOUND:
                        self.backward_bulk_count += 1
                        self.backward_bulk_packet_count += self.backward_bulk_count_tmp
                        self.backward_bulk_size += self.backward_bulk_size_tmp
                        self.backward_bulk_duration += (
                            packet.time - self.backward_bulk_start_tmp
                        )
                    elif self.backward_bulk_count_tmp > constants.BULK_BOUND:
                        self.backward_bulk_packet_count += 1
                        self.backward_bulk_size += payload_size
                        self.backward_bulk_duration += (
                            packet.time - self.backward_bulk_last_timestamp
                        )
                    self.backward_bulk_last_timestamp = packet.time

    @property
    def duration(self):
        return self.latest_timestamp - self.start_timestamp


    


