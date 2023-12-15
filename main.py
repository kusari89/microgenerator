import sys
from PyQt6.QtWidgets import QApplication
from hardware import rb
from control_modem import ControlModem
from hardware import CMD, StatusCMD, ExtTest, Status


def on_packet_received(packet):
    cmd = rb.packet_to_dict(packet)['command']
    data = list(rb.packet_to_dict(packet)['data'])
    print(cmd)
    if cmd == CMD.ping.value:
        window.main_window.status_show('Устройство обнаружено')
        StatusCMD[CMD.ping.name] = False
    elif cmd == CMD.ext.value and data[0] == CMD.test.value:
        print(data[0], data[1])
        if data[1] == ExtTest.get_transceiver_value.value:
            StatusCMD[ExtTest.get_transceiver_value.name] = False
            print(data[0], data[1])
        elif data[1] == ExtTest.get_attenuator_value.value:
            StatusCMD[ExtTest.get_attenuator_value.name] = False
            print(data[0], data[1])
        elif data[1] == ExtTest.get_battery_value.value:
            StatusCMD[ExtTest.get_battery_value.name] = False
            print(data[0], data[1])
        elif data[1] == ExtTest.get_test_alarm.value:
            StatusCMD[ExtTest.get_test_alarm.name] = False
            print(data[0], data[1])
        elif data[1] == ExtTest.get_power_enable.value:
            StatusCMD[ExtTest.get_power_enable.name] = False
            print(data[0], data[1])
        elif data[1] == ExtTest.get_continue_mode.value:
            StatusCMD[ExtTest.get_continue_mode.name] = False
            print(data[0], data[1])
        elif data[1] == ExtTest.test_alarm.value:
            StatusCMD[ExtTest.test_alarm.name] = False
            print(data[0], data[1])
        elif data[1] == ExtTest.power_enable.value:
            StatusCMD[ExtTest.power_enable.name] = False
            print(data[0], data[1])
        elif data[1] == ExtTest.set_continue_mode.value:
            StatusCMD[ExtTest.set_continue_mode.name] = False
            print(data[0], data[1])


if __name__ == '__main__':
    rb.on_packet_received_callback = on_packet_received
    app = QApplication(sys.argv)
    window = ControlModem()
    window.main_window.show()
    app.exec()
