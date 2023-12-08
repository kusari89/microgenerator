from serial import Serial
from serial.threaded import ReaderThread, Protocol
from rb.rb_device import RbDevice


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
    if data is None:
        rb.send_cmd(rb.Address.SENSOR, cmd)
    elif data is not None:
        rb.send_cmd(rb.Address.SENSOR, cmd, data)


def close_port(serial_worker):
    serial_worker.close()







