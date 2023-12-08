import sys

from PyQt6.QtWidgets import QApplication
from Application import MainWindow
from hardware import rb


def on_packet_received(packet):
    cmd = rb.packet_to_dict(packet)['command']
    data = list(rb.packet_to_dict(packet)['data'])
    print(data)
    if cmd == 0x00:
        window.status_show('Устройство обнаружено')
    elif cmd == 0x1E:
        if data[0] == 0x20 and data[1] == 0x06:
            window.set_value_transceiver(data[2])
        elif data[0] == 0x20 and data[1] == 0x07:
            window.set_value_att(data[2])
        elif data[0] == 0x20 and data[1] == 0x08:
            window.set_value_battery(data[2])


if __name__ == '__main__':
    rb.on_packet_received_callback = on_packet_received
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
