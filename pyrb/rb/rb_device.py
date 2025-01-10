from enum import IntEnum
from .dcp2 import *
from .modem import Modem

class RbDevice:
    def __init__(self):
        self.streamer = Streamer()
        self.streamer.on_packet_received_callback = self.process_packet
        self.send_raw_data_callback = None
        self.on_packet_received_callback = None
        self.modem = Modem()
        self.modem.send_packet_callback = lambda pkt: self.__send_raw_data(self.streamer.serialize_packet(pkt))
        self.ping_ok = False

    Address = Packet.Address

    def process_raw_data(self, data: bytearray):
        self.streamer.process_raw_data(data)

    def process_packet(self, packet: Packet):
        if not self.on_packet_received_callback is None:
            self.on_packet_received_callback(packet)

        if packet.address_src:
            if Packet.Address.SENSOR:
                self.ping_ok = True
            elif Packet.Address.MODEM:
                self.ping_ok = True
                self.modem.process_packet(packet)
            else:
                pass

    def send_cmd(self, addr: Packet.Address, cmd: int, data = bytearray()):
        pkt = Packet()
        pkt.address_src = Packet.Address.PC
        pkt.address_dst = addr
        pkt.command = cmd & 0xFF
        pkt.data = data
        self.__send_raw_data(self.streamer.serialize_packet(pkt))

    def send_cmd_ping(self, addr: Packet.Address):
        self.send_cmd(addr, 0)
    
    def send_cmd_ping_modem(self):
        self.send_cmd_ping(Packet.Address.MODEM)
    
    def send_cmd_ping_sensor(self):
        self.send_cmd_ping(Packet.Address.SENSOR)

    @property
    def rx_packet_counter(self):
        return self.streamer.rx_packet_counter
    
    @property
    def rx_bad_packet_counter(self):
        return self.streamer.rx_bad_packet_counter
    
    @property
    def tx_packet_counter(self):
        return self.streamer.tx_packet_counter

    def packet_to_dict(self, packet: Packet):
        return dict({'address_dst': packet.address_dst, 'address_src': packet.address_src, 'command': packet.command,
            'response': packet.response, 'is_response': packet.is_response, 'data': list(packet.data)})

    def __send_raw_data(self, data: bytearray):
        if self.send_raw_data_callback:
            self.send_raw_data_callback(data)



