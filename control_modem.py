from Application import MainWindow
import hardware as hw
import serial.tools.list_ports
import struct
from PyQt6.QtCore import QTimer
import threading


class ControlModem:
    def __init__(self):
        self.main_window = MainWindow()
        self.serial_worker = None

    # подключенные сигналы
        # сигнал кнопки ком порта
        self.main_window.com_parameters.com_status.clicked.connect(self.start_work)
        # Сигналы блока общего управления
        self.main_window.general_management.request.clicked.connect(self.request_all_param)
        self.main_window.general_management.default.clicked.connect(self.default_all_param)
        # Сигналы от блока настройки частоты
        self.main_window.freq_options.install_parameters.clicked.connect(self.send_display_parameters)
        self.main_window.freq_options.manual_edit.clicked.connect(self.display_manual_parameters)

    '''
    Метод запускает работу программы. Открывает компорт, а если ком порт открыт, то закрывает его. 
    Ориентируется на текущее состояние кнопки com_status. 
    '''

    def start_work(self, checked):
        com_name = self.main_window.com_parameters.com_list.currentText()
        if checked:
            # Сигнал от радиокнопки
            self.main_window.transceiver_power.button_group.buttonClicked.connect(self.set_value_transceiver)
            try:
                self.serial_worker = hw.open_port(com_name)
            except serial.serialutil.SerialException:
                self.main_window.status_show(f'Ошибка открытия {com_name}')
                self.main_window.com_parameters.com_status.setChecked(False)
            else:
                hw.send_message(hw.CMD.ping)
                self.main_window.funk_enable.test.stateChanged.connect(self.test_enable)
                self.main_window.funk_enable.full_power.stateChanged.connect(self.full_power_enable)
                self.main_window.funk_enable.continue_mode.stateChanged.connect(self.continue_mode_enable)
                self.main_window.enable_all_element(checked)
                self.main_window.status_show(f' {com_name} открыт')
                self.request_all_param()
        else:
            hw.close_port(self.serial_worker)
            self.main_window.transceiver_power.button_group.buttonClicked.disconnect()
            self.main_window.funk_enable.test.stateChanged.disconnect()
            self.main_window.funk_enable.full_power.stateChanged.disconnect()
            self.main_window.funk_enable.continue_mode.stateChanged.disconnect()
            self.main_window.enable_all_element(checked)
            self.serial_worker = None
            self.main_window.status_show(f' {com_name} закрыт')

    '''
    Метод запускает функцию "тест" на микрогенераторе
    '''

    @staticmethod
    def test_enable(status):
        if status == 2:
            hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.test_alarm, hw.Status.on])
        else:
            hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.test_alarm, hw.Status.off])

    '''
    Метод запрашивает все текущие параметры микрогенератора
    '''

    @staticmethod
    def request_all_param():
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_transceiver_value])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_attenuator_value])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_battery_value])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_test_alarm])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_power_enable])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_continue_mode])
        hw.send_message(hw.CMD.rsl_parameters, hw.RslParam.get_rsl_param)

    def default_all_param(self):
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.set_transceiver, 0])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.set_attenuator, 0])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.set_continue_mode, hw.Status.off])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.power_enable, hw.Status.off])
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.test_alarm, hw.Status.off])
        self.request_all_param()

    '''
    Метод запускает функцию "full_power" на микрогенераторе, при снятии флага метод отправляет 
    текущие установленные настройки трансивера и аттенюатора
    '''

    def full_power_enable(self, status):
        if status == 2:
            hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.power_enable, hw.Status.on])
        else:
            value_pwr = self.main_window.transceiver_power.button_group.checkedButton().text()
            value_att = self.main_window.att_current.att_slider.value()
            hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.power_enable, hw.Status.off])
            self.send_current_transceiver(value_pwr)
            self.send_current_attenuator(value_att)

    '''
    Метод запускает функцию "continue_mode" на микрогенераторе, при снятии флага метод отправляет 
    текущие установленные настройки трансивера и аттенюатора
    '''
    def continue_mode_enable(self, status):
        if status == 2:
            hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.set_continue_mode, hw.Status.on])
        else:
            value_pwr = self.main_window.transceiver_power.button_group.checkedButton().text()
            value_att = self.main_window.att_current.att_slider.value()
            hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.set_continue_mode, hw.Status.off])
            self.send_current_transceiver(value_pwr)
            self.send_current_attenuator(value_att)

    def send_current_transceiver(self, value):
        value = self.main_window.transceiver_power.buttons_values_send[value.split()[0]]
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.set_transceiver, value])

    @staticmethod
    def send_current_attenuator(value):
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.set_attenuator, value])

    def set_value_transceiver(self, button):
        self.main_window.att_current.transceiver_power = button.text()
        self.main_window.att_current.value_changed(self.main_window.att_current.att_slider.value())
        self.send_current_transceiver(button.text())

    def send_display_parameters(self):
        clock_freq = int(float(self.main_window.freq_options.clock_freq.text())*100)
        carrier_freq = int(float(self.main_window.freq_options.carrier_freq.text()))
        data = bytearray(struct.pack('<LH', carrier_freq, clock_freq)) + bytearray(10)
        self.main_window.freq_options.carrier_freq.setStyleSheet("QLineEdit { color: black; background-color: white;}")
        self.main_window.freq_options.clock_freq.setStyleSheet("QLineEdit { color: black; background-color: white;}")
        hw.send_message(hw.CMD.rsl_parameters, [hw.RslParam.set_rsl_param, data])

    def fuck_low_power(self):
        hw.send_message(hw.CMD.ext, [hw.CMD.test, hw.ExtTest.get_battery_value])
        if hw.StatusCMD[hw.ExtTest.low_power_notify.name] is True:
            self.main_window.battery.battery_status.setStyleSheet("QLineEdit { color: black; background-color: red;}")

    def display_manual_parameters(self, checked):
        if checked:
            self.main_window.freq_options.display_manual_parameters(checked)
        else:
            if self.main_window.freq_options.display_manual_parameters(checked):
                self.send_display_parameters()
                hw.send_message(hw.CMD.rsl_parameters, hw.RslParam.get_rsl_param)
            else:
                pass


