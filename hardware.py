from serial import Serial
from serial.threaded import ReaderThread, Protocol
from rb.rb_device import RbDevice
from enum import Enum
import time

rb = RbDevice()


class SerialReader(Protocol):
    def connection_made(self, transport):
        print("Connected, ready to receive data...")

    def data_received(self, data):
        rb.process_raw_data(data)

    def connection_lost(self, exc):
        print("Connection lost... Error: " + str(exc))


def open_port(number_port):
    serial_port = Serial(number_port, 4800)
    serial_worker = ReaderThread(serial_port, SerialReader)
    serial_worker.start()
    rb.send_raw_data_callback = serial_port.write
    return serial_worker


def send_message(cmd, data=None):
    counter = 0
    if data is None:
        StatusCMD[cmd.name] = True
        while StatusCMD[cmd.name] is True:
            rb.send_cmd(rb.Address.SENSOR, cmd.value)
            time.sleep(0.1)
            counter += 1
            if counter > 2:
                break
    elif type(data) == bytearray:
        rb.send_cmd(rb.Address.SENSOR, cmd, data)
    elif type(data) in (CMD, ExtTest, Status, RslParam):
        StatusCMD[data.name] = True
        rb.send_cmd(rb.Address.SENSOR, cmd.value, bytearray([data.value]))
    elif type(data) == list:
        if data[0] == CMD.test:
            StatusCMD[data[1].name] = True
            send_data = bytearray()
            for symbol in data:
                if type(symbol) in (CMD, ExtTest, Status, RslParam):
                    send_data += bytearray([symbol.value])
                elif type(symbol) == int:
                    send_data += bytearray([symbol])
                elif type(symbol) == bytearray:
                    send_data += symbol
            while StatusCMD[data[1].name] is True:
                send_data_temp = send_data
                rb.send_cmd(rb.Address.SENSOR, cmd.value, send_data_temp)
                time.sleep(0.15)
                counter += 1
                if counter > 2:
                    return
        elif data[0] == RslParam.set_rsl_param:
            StatusCMD[data[0].name] = True
            send_data = bytearray()
            for symbol in data:
                if type(symbol) in (CMD, ExtTest, Status, RslParam):
                    send_data += bytearray([symbol.value])
                elif type(symbol) == int:
                    send_data += bytearray([symbol])
                elif type(symbol) == bytearray:
                    send_data += symbol
            while StatusCMD[data[0].name] is True:
                rb.send_cmd(rb.Address.SENSOR, cmd.value, send_data)
                time.sleep(0.15)
                counter += 1
                if counter > 2:
                    return


def close_port(serial_worker):
    serial_worker.close()


StatusCMD = {
    'ping': False,
    'test_alarm': False,
    'get_test_alarm': False,
    'power_enable': False,
    'get_power_enable': False,
    'set_transceiver': False,
    'get_transceiver_value': False,
    'set_attenuator': False,
    'get_attenuator_value': False,
    'low_power_notify': False,
    'get_battery_value': False,
    'set_continue_mode': False,
    'get_continue_mode': False,
    'set_rsl_param': False,
    'get_rsl_param': False,
            }


class CMD(Enum):
    ping = 0x00
    ext = 0x1E
    test = 0x20
    rsl_parameters = 0x1D


class RslParam(Enum):
    get_rsl_param = 0x23
    set_rsl_param = 0x24


class ExtTest(Enum):
    test_alarm = 0x01
    get_test_alarm = 0x0B
    power_enable = 0x02
    get_power_enable = 0x0C
    set_transceiver = 0x03
    get_transceiver_value = 0x06
    set_attenuator = 0x04
    get_attenuator_value = 0x07
    low_power_notify = 0x05
    get_battery_value = 0x08
    set_continue_mode = 0x09
    get_continue_mode = 0x0A


class Status(Enum):
    on = 0x01
    off = 0x00

