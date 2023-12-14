from Application import MainWindow
import hardware as hw
import serial.tools.list_ports


class ControlModem:
    def __init__(self):
        self.main_window = MainWindow()
        self.serial_worker = None

    # подключенные сигналы
        self.main_window.com_parameters.com_status.clicked.connect(self.start_work)

    def start_work(self, checked):
        com_name = self.main_window.com_parameters.com_list.currentText()
        self.main_window.enable_all_element(checked)
        if checked:
            try:
                self.serial_worker = hw.open_port(com_name)
                hw.send_message(hw.CMD.ping)
                self.main_window.status_show(f' {com_name} открыт')
            except serial.serialutil.SerialException:
                self.main_window.status_show(f'Ошибка открытия {com_name}')
        else:
            hw.close_port(self.serial_worker)
            self.serial_worker = None
            self.main_window.status_show(f' {com_name} закрыт')
        self.get_start_data()

    @staticmethod
    def get_start_data():
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_transceiver_value])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_attenuator_value])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_battery_value])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_test_alarm])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_power_enable])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_continue_mode])
