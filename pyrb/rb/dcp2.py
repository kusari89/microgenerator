from enum import IntEnum

HEADER_SIZE = 4
CHECKSUM_INIT = 0x89

class Packet:
    """DCP2 packet structure"""
    class Address(IntEnum):
        PC      = 0x00
        SENSOR  = 0x01
        MODEM   = 0x02
        VC      = 0x03
        ALL     = 0x0F

    class Response(IntEnum):
        Okay    = 0  # Успешное выполнение
        Error   = 1  # Ошибка при выполнении
        Busy    = 2  # Устройство занято (можно повторить запрос позже)
        Nak     = 3  # Нет устройства под данным номером или оно неисправно

    def __init__(self):
        self.address_dst = self.Address.ALL
        """Адрес приемника"""
        self.address_src = self.Address.ALL
        """Адрес источника"""
        self.command = 0
        """Код команды"""
        self.response = self.Response.Okay
        """Код подтверждения"""
        self.is_response = False
        """Флаг "Запрос"/"Ответ" (0 - запрос / уведомление, 1 - ответ)"""
        self.data = bytearray()
        """Данные"""

class Streamer:
    """Сериализация/десериализация пакетов DCP2"""
    def __init__(self):
        self.on_packet_received_callback = None
        """Callback вызываемый при обнаружении пакета в потоке данных"""
        self.on_bad_packet_received_callback = None
        """Callback вызываемый при обнаружении пакета с неверной контрольной суммой"""
        self.rx_packet_counter = 0
        """Счётчик принятых пакетов"""
        self.rx_bad_packet_counter = 0
        """Счётчик принятых пакетов с неверной контрольной суммой"""
        self.tx_packet_counter = 0
        """Счётчик отправленных пакетов"""
        self.__rxData = bytearray()
    
    def process_raw_data(self, data: bytearray):
        self.__rxData += data
        while len(self.__rxData) >= HEADER_SIZE:
            packet = self.__unpack_header(self.__rxData)
            if packet is None:
                del self.__rxData[0]
            else:
                packetSize = HEADER_SIZE + len(packet.data) + int(len(packet.data) > 0)
                if len(self.__rxData) >= packetSize:
                    packet.data = self.__rxData[HEADER_SIZE:packetSize-1]
                    cs_calc = sum(packet.data, self.__rxData[3]) & 0xFF
                    cs_recv = self.__rxData[packetSize-1:packetSize][0]
                    if cs_calc == cs_recv:
                        self.rx_packet_counter += 1
                        packet.data = self.__rxData[HEADER_SIZE:packetSize-1]
                        self.__rxData = self.__rxData[packetSize:]
                        if self.on_packet_received_callback:
                            self.on_packet_received_callback(packet)
                    else:
                        self.rx_bad_packet_counter += 1
                        self.__rxData = self.__rxData[HEADER_SIZE:]
                        if self.on_bad_packet_received_callback:
                            self.on_bad_packet_received_callback(self.__rxData[:packetSize])
                else:
                    break
    
    def serialize_packet(self, packet: Packet):
        data = bytearray(HEADER_SIZE)
        data[0] = ((packet.address_dst & 0x0F) + ((packet.address_src & 0x0F) << 4)) & 0xFF
        data[1] = ((packet.command & 0x1F) + (packet.response << 5) & 0xFF + (packet.is_response << 7) & 0xFF) & 0xFF
        data[2] = len(packet.data) & 0xFF
        data[3] = sum(data[:3], CHECKSUM_INIT) & 0xFF
        if len(packet.data) > 0:
            packet.data.append(sum(packet.data, data[3]) & 0xFF)
        data += packet.data
        self.tx_packet_counter += 1
        return data
    
    def __unpack_header(self, data):
        if (data[3] == sum(data[:3], CHECKSUM_INIT) & 0xFF):
            packet = Packet()
            packet.address_dst = Packet.Address( data[0] & 0x0F)
            packet.address_src = Packet.Address((data[0] & 0xF0) >> 4)
            packet.command = data[1] & 0x1F
            packet.response = Packet.Response((data[1] >> 5) & 0x03)
            packet.is_response = bool((data[1] >> 7) & 0x01)
            packet.data = bytearray(data[2])
            return packet
        else:
            return None