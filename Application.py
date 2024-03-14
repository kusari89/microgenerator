from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QSlider,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QButtonGroup,
)
import struct
import PyQt6.QtGui
import serial.tools.list_ports
import configparser
import hardware


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Микрогенератор")
        self.setWindowIcon(PyQt6.QtGui.QIcon('орден нытика.jpg'))

        self.statusBar()
        self.status_show('Программа запущена')

        self.com_parameters = ComParameters()
        self.general_management = GeneralManagement()
        self.att_current = AttCurrent()
        self.transceiver_power = TransceiverPower()
        self.funk_enable = FunkEnable()
        self.battery = Battery()
        self.freq_options = FreqOptions()

        layout_left = QVBoxLayout()
        layout_left.addWidget(self.com_parameters)
        layout_left.addWidget(self.transceiver_power)

        layout_middle = QVBoxLayout()
        layout_middle.addWidget(self.general_management)
        layout_middle.addWidget(self.att_current)

        layout_left_main = QHBoxLayout()
        layout_left_main.addLayout(layout_left)
        layout_left_main.addLayout(layout_middle)

        layout_right_top = QHBoxLayout()
        layout_right_top.addWidget(self.funk_enable)
        layout_right_top.addWidget(self.battery)

        layout_right_bot = QHBoxLayout()
        layout_right_bot.addWidget(self.freq_options)

        layout_right = QVBoxLayout()
        layout_right.addLayout(layout_right_top)
        layout_right.addLayout(layout_right_bot)

        layout_main = QHBoxLayout()
        layout_main.addLayout(layout_left_main)
        layout_main.addLayout(layout_right)

        container = QWidget()
        container.setLayout(layout_main)
        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)
        self.setFixedSize(800, 340)

    def status_show(self, text):
        self.statusBar().showMessage(text)

    def enable_all_element(self, checked):
        self.com_parameters.enable_all_element(checked)
        self.general_management.enable_all_element(checked)
        self.transceiver_power.enable_all_element(checked)
        self.att_current.enable_all_element(checked)
        self.funk_enable.enable_all_element(checked)
        self.battery.enable_all_element(checked)
        self.freq_options.enable_all_element(checked)

    def set_value_transceiver(self, value):
        self.transceiver_power.set_value_transceiver(value)

    def set_value_att(self, value):
        self.att_current.set_value_att(value)

    def set_value_battery(self, value):
        self.battery.set_value_battery(value)


class ComParameters(QWidget):
    def __init__(self):
        super().__init__()
        self.com_list = QComboBox()
        com_list = [element.device for element in serial.tools.list_ports.comports()]
        com_list.sort()
        self.com_list.addItems(com_list)

        self.com_status = QPushButton('Открыть')
        self.com_status.setCheckable(True)

        port_label = QLabel('Порт')
        groupbox = QGroupBox(port_label.text())
        groupbox.setFixedSize(150, 110)

        group_layout = QVBoxLayout(groupbox)
        group_layout.addWidget(self.com_list)
        group_layout.addWidget(self.com_status)

        lay = QVBoxLayout()
        lay.addWidget(groupbox)
        self.setLayout(lay)

    def enable_all_element(self, checked):
        if checked:
            self.com_status.setChecked(True)
            self.com_status.setText('Закрыть')
            self.com_list.setDisabled(True)
        else:
            self.com_status.setChecked(False)
            self.com_status.setText('Открыть')
            self.com_list.setEnabled(True)


class FunkEnable(QWidget):
    def __init__(self):
        super().__init__()
        self.test = QCheckBox('TEST')
        self.test.setDisabled(True)

        self.full_power = QCheckBox('FULL POWER')
        self.full_power.setDisabled(True)

        self.continue_mode = QCheckBox('CONTINUE MODE')
        self.continue_mode.setDisabled(True)

        funk_enable_label = QLabel('Активация функций')
        groupbox = QGroupBox(funk_enable_label.text())
        groupbox.setFixedSize(150, 110)

        group_layout = QVBoxLayout(groupbox)
        group_layout.addWidget(self.test)
        group_layout.addWidget(self.full_power)
        group_layout.addWidget(self.continue_mode)

        lay = QVBoxLayout()
        lay.addWidget(groupbox)
        self.setLayout(lay)

    def enable_all_element(self, checked):
        if checked:
            self.test.setEnabled(True)
            self.full_power.setEnabled(True)
            self.continue_mode.setEnabled(True)
        else:
            self.test.setChecked(False)
            self.full_power.setChecked(False)
            self.continue_mode.setChecked(False)
            self.test.setDisabled(True)
            self.full_power.setDisabled(True)
            self.continue_mode.setDisabled(True)


class TransceiverPower(QWidget):
    def __init__(self):
        super().__init__()
        self.radiobutton_power_1 = QRadioButton('+10 dB')
        self.radiobutton_power_2 = QRadioButton('  0 dB')
        self.radiobutton_power_3 = QRadioButton('-10 dB')
        self.radiobutton_power_4 = QRadioButton('-20 dB')
        self.radiobutton_power_5 = QRadioButton('-30 dB')

        self.buttons_values = {
            "10": self.radiobutton_power_1,
            "0": self.radiobutton_power_2,
            "246": self.radiobutton_power_3,
            "236": self.radiobutton_power_4,
            "226": self.radiobutton_power_5,
        }
        self.buttons_values_send = {
            "+10": 10,
            "0": 0,
            "-10": 246,
            "-20": 236,
            "-30": 226,
        }

        self.radiobutton_power_1.setDisabled(True)
        self.radiobutton_power_2.setDisabled(True)
        self.radiobutton_power_3.setDisabled(True)
        self.radiobutton_power_4.setDisabled(True)
        self.radiobutton_power_5.setDisabled(True)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radiobutton_power_1)
        self.button_group.addButton(self.radiobutton_power_2)
        self.button_group.addButton(self.radiobutton_power_3)
        self.button_group.addButton(self.radiobutton_power_4)
        self.button_group.addButton(self.radiobutton_power_5)

        transceiver_power_label = QLabel('Мощность трансивера')
        groupbox = QGroupBox(transceiver_power_label.text())

        group_layout = QVBoxLayout(groupbox)
        group_layout.addWidget(self.radiobutton_power_1)
        group_layout.addWidget(self.radiobutton_power_2)
        group_layout.addWidget(self.radiobutton_power_3)
        group_layout.addWidget(self.radiobutton_power_4)
        group_layout.addWidget(self.radiobutton_power_5)

        lay = QVBoxLayout()
        lay.addWidget(groupbox)
        self.setLayout(lay)

    def enable_all_element(self, checked):
        if checked:
            self.radiobutton_power_1.setEnabled(True)
            self.radiobutton_power_2.setEnabled(True)
            self.radiobutton_power_3.setEnabled(True)
            self.radiobutton_power_4.setEnabled(True)
            self.radiobutton_power_5.setEnabled(True)
            self.radiobutton_power_2.setChecked(True)
        else:
            self.radiobutton_power_1.setDisabled(True)
            self.radiobutton_power_2.setDisabled(True)
            self.radiobutton_power_3.setDisabled(True)
            self.radiobutton_power_4.setDisabled(True)
            self.radiobutton_power_5.setDisabled(True)
            self.radiobutton_power_1.setChecked(False)
            self.radiobutton_power_2.setChecked(False)
            self.radiobutton_power_3.setChecked(False)
            self.radiobutton_power_4.setChecked(False)
            self.radiobutton_power_5.setChecked(False)

    def set_value_transceiver(self, value):
        button = self.buttons_values[str(value)]
        button.setChecked(True)


class AttCurrent(QWidget):
    def __init__(self):
        super().__init__()
        self.transceiver_power = '0 dB'

        self.att_slider = QSlider()
        self.att_slider.setMinimum(0)
        self.att_slider.setMaximum(63)
        self.att_slider.setPageStep(1)
        self.att_slider.setSingleStep(1)

        self.att_current = QLineEdit('')
        self.att_current.setReadOnly(True)
        att_current_label = QLabel('Значение аттенюатора')

        self.pwr_current = QLineEdit('')
        self.pwr_current.setReadOnly(True)
        pwr_current_label = QLabel('Выходная мощность')

        self.att_slider.setDisabled(True)
        self.att_current.setDisabled(True)
        self.pwr_current.setDisabled(True)

        layout_info = QVBoxLayout()
        layout_info.addWidget(att_current_label)
        layout_info.addWidget(self.att_current)
        layout_info.addWidget(pwr_current_label)
        layout_info.addWidget(self.pwr_current)

        att_lvl_label = QLabel('Настройки аттенюатора')
        groupbox = QGroupBox(att_lvl_label.text())
        group_layout = QHBoxLayout(groupbox)
        group_layout.addWidget(self.att_slider)
        group_layout.addLayout(layout_info)

        main_layout = QVBoxLayout(groupbox)
        main_layout.addWidget(groupbox)
        self.setLayout(main_layout)

        self.att_slider.sliderPressed.connect(self.slider_pressed)
        self.att_slider.sliderReleased.connect(self.slider_released)
        self.att_slider.valueChanged.connect(self.value_changed)

    def enable_all_element(self, checked):
        if checked:
            self.att_slider.setEnabled(True)
            self.att_current.setEnabled(True)
            self.pwr_current.setEnabled(True)
        else:
            self.att_slider.valueChanged.disconnect()
            self.att_slider.setValue(0)
            self.att_current.setText('')
            self.pwr_current.setText('')
            self.att_slider.setDisabled(True)
            self.att_current.setDisabled(True)
            self.pwr_current.setDisabled(True)

    def slider_pressed(self):
        self.att_slider.valueChanged.disconnect()
        self.att_slider.valueChanged.connect(self.value_changed_second)
        self.att_current.setStyleSheet("QLineEdit { color: black; background-color: yellow;}")
        self.pwr_current.setStyleSheet("QLineEdit { color: black; background-color: yellow;}")

    def slider_released(self):
        data = bytearray([0x20, 0x04, int(self.att_slider.value())])
        hardware.send_message(0x1E, data)
        self.att_slider.valueChanged.disconnect()
        self.att_slider.valueChanged.connect(self.value_changed)
        self.att_current.setStyleSheet("QLineEdit { color: black; background-color: white;}")
        self.pwr_current.setStyleSheet("QLineEdit { color: black; background-color: white;}")

    def value_changed(self, value):
        self.att_current.setText(str(value/2) + ' dB')
        pwr_value = -60 + float(self.transceiver_power.split()[0]) - float(value)/2
        self.pwr_current.setText(str(pwr_value) + ' dBm')
        data = bytearray([0x20, 0x04, int(value)])
        hardware.send_message(0x1E, data)

    def value_changed_second(self):
        self.att_current.setText(str(self.att_slider.value() / 2) + ' dB')
        pwr_value = -60 + float(self.transceiver_power.split()[0]) - float(self.att_slider.value()) / 2
        self.pwr_current.setText(str(pwr_value) + ' dBm')

    def set_value_att(self, value):
        self.att_slider.setValue(value)


class GeneralManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.request = QPushButton('Запросить все настройки')
        self.request.setDisabled(True)
        self.default = QPushButton('Установить по умолчанию')
        self.default.setDisabled(True)

        general_management_label = QLabel('Общее упавление')
        groupbox = QGroupBox(general_management_label.text())
        groupbox.setFixedSize(190, 110)

        group_layout = QVBoxLayout(groupbox)
        group_layout.addWidget(self.request)
        group_layout.addWidget(self.default)

        lay = QVBoxLayout()
        lay.addWidget(groupbox)

        self.setLayout(lay)

    def enable_all_element(self, checked):
        if checked:
            self.request.setEnabled(True)
            self.default.setEnabled(True)
        else:
            self.request.setDisabled(True)
            self.default.setDisabled(True)


class FreqOptions(QWidget):
    def __init__(self):
        super().__init__()

        self.config = configparser.ConfigParser()
        self.config.read('parameters.ini')

        self.letter = QComboBox()
        self.letter.addItems(self.config.sections())
        letter_number_label = QLabel('Литера №')
        self.letter.setCurrentIndex(-1)

        self.install_parameters = QPushButton('Установить')

        self.carrier_freq = QLineEdit()
        self.carrier_freq.setReadOnly(True)
        self.carrier_freq.setFixedSize(238, 25)
        carrier_freq_label = QLabel('Несущая частота')

        self.clock_freq = QLineEdit()
        self.clock_freq.setReadOnly(True)
        self.clock_freq.setFixedSize(238, 25)
        clock_freq_label = QLabel('Тактовая частота')

        self.manual_edit = QPushButton('Редактировать частоты вручную')

        self.letter.setDisabled(True)
        self.install_parameters.setDisabled(True)
        self.carrier_freq.setDisabled(True)
        self.clock_freq.setDisabled(True)
        self.manual_edit.setDisabled(True)

        letter_layout = QHBoxLayout()
        letter_layout.addWidget(letter_number_label)
        letter_layout.addWidget(self.letter)
        letter_layout.addWidget(self.install_parameters)

        carrier_freq_layout = QHBoxLayout()
        carrier_freq_layout.addWidget(carrier_freq_label)
        carrier_freq_layout.addWidget(self.carrier_freq)

        clock_freq_layout = QHBoxLayout()
        clock_freq_layout.addWidget(clock_freq_label)
        clock_freq_layout.addWidget(self.clock_freq)

        freq_options_label = QLabel('Настройка частот')
        groupbox = QGroupBox(freq_options_label.text())
        groupbox.setFixedSize(380, 150)

        group_layout = QVBoxLayout(groupbox)
        group_layout.addLayout(letter_layout)
        group_layout.addLayout(carrier_freq_layout)
        group_layout.addLayout(clock_freq_layout)
        group_layout.addWidget(self.manual_edit)

        lay = QVBoxLayout()
        lay.addWidget(groupbox)

        self.setLayout(lay)

        self.letter.currentTextChanged.connect(self.display_new_parameters)
        self.manual_edit.clicked.connect(self.display_manual_parameters)

    def enable_all_element(self, checked):
        if checked:
            self.letter.setEnabled(True)
            self.install_parameters.setEnabled(True)
            self.carrier_freq.setEnabled(True)
            self.clock_freq.setEnabled(True)
            self.manual_edit.setEnabled(True)
        else:
            self.letter.currentTextChanged.disconnect()
            self.letter.setCurrentIndex(-1)
            self.carrier_freq.setText('')
            self.clock_freq.setText('')
            self.letter.setDisabled(True)
            self.install_parameters.setDisabled(True)
            self.carrier_freq.setDisabled(True)
            self.clock_freq.setDisabled(True)
            self.manual_edit.setDisabled(True)

    def set_display_parameters(self, data):
        self.letter.currentTextChanged.disconnect(self.display_new_parameters)
        data = bytearray(data)
        data = struct.unpack('<cLHHLHH', data)
        self.carrier_freq.setText(str(data[1]))
        self.clock_freq.setText(str(data[2]/100))
        for section in self.config.sections():
            if str(data[1]) == self.config[section]['carrierFrequency_kHz'] \
                    and str(data[2]) == self.config[section]['clockRate_x100']:
                self.letter.setCurrentText(section)
                break
            else:
                self.letter.setCurrentIndex(-1)
        self.carrier_freq.setStyleSheet("QLineEdit { color: black; background-color: white;}")
        self.clock_freq.setStyleSheet("QLineEdit { color: black; background-color: white;}")
        self.letter.currentTextChanged.connect(self.display_new_parameters)

    def display_new_parameters(self):
        self.carrier_freq.setText(self.config[f'{self.letter.currentText()}']['carrierFrequency_kHz'])
        self.clock_freq.setText(str(float(self.config[f'{self.letter.currentText()}']['clockRate_x100']) / 100))
        self.carrier_freq.setStyleSheet("QLineEdit { color: black; background-color: yellow;}")
        self.clock_freq.setStyleSheet("QLineEdit { color: black; background-color: yellow;}")

    def display_manual_parameters(self):
        self.manual_edit.setText('Эта функция еще не работает ;-)')


class Battery(QWidget):
    def __init__(self):
        super().__init__()
        self.battery_lvl = QLineEdit()
        self.battery_lvl.setFixedSize(100, 25)
        self.battery_lvl.setReadOnly(True)
        self.battery_lvl.setDisabled(True)
        battery_lvl_label = QLabel('Напряжение')

        self.battery_status = QLineEdit()
        self.battery_status.setFixedSize(100, 25)
        self.battery_status.setReadOnly(True)
        self.battery_status.setDisabled(True)
        battery_status_label = QLabel('Статус')

        battery_lvl_layout = QHBoxLayout()
        battery_lvl_layout.addWidget(battery_lvl_label)
        battery_lvl_layout.addWidget(self.battery_lvl)

        battery_status_layout = QHBoxLayout()
        battery_status_layout.addWidget(battery_status_label)
        battery_status_layout.addWidget(self.battery_status)

        battery_label = QLabel('Состояние батареи')
        groupbox = QGroupBox(battery_label.text())

        group_layout = QVBoxLayout(groupbox)
        group_layout.addLayout(battery_lvl_layout)
        group_layout.addLayout(battery_status_layout)

        lay = QVBoxLayout()
        lay.addWidget(groupbox)
        self.setLayout(lay)

    def enable_all_element(self, checked):
        if checked:
            self.battery_lvl.setEnabled(True)
            self.battery_status.setEnabled(True)
        else:
            self.battery_lvl.setText('')
            self.battery_status.setText('')
            self.battery_lvl.setDisabled(True)
            self.battery_status.setDisabled(True)

    def set_value_battery(self, value):
        self.battery_lvl.setText(str(value) + ' В')
        if 11 > value >= 8:
            self.battery_status.setText('Норма')
            self.battery_status.setStyleSheet("QLineEdit { color: black; background-color: white;}")
        elif 8 > value > 6:
            self.battery_status.setText('Заменить')
            self.battery_status.setStyleSheet("QLineEdit { color: black; background-color: yellow;}")
        elif 5 >= value:
            self.battery_status.setText('Заменить')
            self.battery_status.setStyleSheet("QLineEdit { color: black; background-color: red;}")
        if hardware.StatusCMD[hardware.ExtTest.low_power_notify.name] is True:
            self.battery_status.setStyleSheet("QLineEdit { color: black; background-color: red;}")
