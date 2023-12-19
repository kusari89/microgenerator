import sys
from PyQt6.QtWidgets import QApplication
from hardware import rb
from control_modem import ControlModem
from hardware import CMD, StatusCMD, ExtTest, Status


def on_packet_received(packet):
    cmd = rb.packet_to_dict(packet)['command']
    data = list(rb.packet_to_dict(packet)['data'])
    if cmd == CMD.ping.value:
        window.main_window.status_show('Устройство обнаружено')
        StatusCMD[CMD.ping.name] = False
    elif cmd == CMD.ext.value and data[0] == CMD.test.value:
        print(data)
        if data[1] == ExtTest.get_transceiver_value.value:
            StatusCMD[ExtTest.get_transceiver_value.name] = False
            window.main_window.transceiver_power.set_value_transceiver(data[2])
        elif data[1] == ExtTest.get_attenuator_value.value:
            StatusCMD[ExtTest.get_attenuator_value.name] = False
            window.main_window.att_current.set_value_att(data[2])
        elif data[1] == ExtTest.get_battery_value.value:
            StatusCMD[ExtTest.get_battery_value.name] = False
            window.main_window.battery.set_value_battery(data[2])
        elif data[1] == ExtTest.get_test_alarm.value:
            StatusCMD[ExtTest.get_test_alarm.name] = False
            if data[2] == 0:
                window.main_window.funk_enable.test.setChecked(False)
            else:
                window.main_window.funk_enable.test.setChecked(True)
        elif data[1] == ExtTest.get_power_enable.value:
            StatusCMD[ExtTest.get_power_enable.name] = False
            if data[2] == 0:
                window.main_window.funk_enable.full_power.setChecked(False)
            else:
                window.main_window.funk_enable.full_power.setChecked(True)
        elif data[1] == ExtTest.get_continue_mode.value:
            StatusCMD[ExtTest.get_continue_mode.name] = False
            if data[2] == 0:
                window.main_window.funk_enable.continue_mode.setChecked(False)
            else:
                window.main_window.funk_enable.continue_mode.setChecked(True)
        elif data[1] == ExtTest.test_alarm.value:
            StatusCMD[ExtTest.test_alarm.name] = False
        elif data[1] == ExtTest.power_enable.value:
            StatusCMD[ExtTest.power_enable.name] = False
        elif data[1] == ExtTest.set_continue_mode.value:
            StatusCMD[ExtTest.set_continue_mode.name] = False
        elif data[1] == ExtTest.set_attenuator.value:
            StatusCMD[ExtTest.set_attenuator.name] = False
        elif data[1] == ExtTest.set_transceiver.value:
            StatusCMD[ExtTest.set_transceiver.name] = False


if __name__ == '__main__':
    rb.on_packet_received_callback = on_packet_received
    app = QApplication(sys.argv)
    window = ControlModem()
    window.main_window.show()
    app.exec()
