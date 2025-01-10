from enum import IntEnum
from .dcp2 import Packet


class Modem:
    def __init__(self):
        self.send_packet_callback = None
        self.info = {int: self.Info}
        self.link_info = {int: self.LinkInfo}
        self.self_net_address = -1
        self.route_table = [bytearray()]

    class Command(IntEnum):
        PING        = 0x00  # Пинг
        WHO_ARE_YOU = 0x01  # Запрос версии ПО
        DATA        = 0x08  # Данные принятые по радиоканалу
        TEXT        = 0x09  # Запрос версии ПО
        SYS         = 0x0A  # Системная информация
        SEND_DEF    = 0x10  # Отправить данные в эфир, адресат по умолчанию
        SEND_ADDR	= 0x11  # Отправить данные в эфир, на указанный адрес
        DO			= 0x12  # Команда модему
        TEST		= 0x13  # Тестовые команды модема
    
    class CmdDo(IntEnum):
        """Список подкоманд группы ModemCmdDo."""
        STBY_MODE                   = 0x01  # Перевод модема в режим ожидания
        SHOW_STATUS                 = 0x02  # Запрос состояния "своего" модема
        SHOW_LINX                   = 0x05  # Запрос данных о слышимости для определенного узла
        SHOW_ROUTE                  = 0x07  # Запрос маршрутной таблицы
        SET_XTYP                    = 0x08  # Установка типа ВУ модему
        NORMAL_MODE                 = 0x09  # Перевод модема в нормальный режим работы
        SET_MODE                    = 0x0A  # Установка редима работы модема
        ASK_STATUS                  = 0x0C  # Запрос состояния удалённого модема
        GET_MODEM_VERSION_REMOTE    = 0x0F  # Запрос версии удалённого модема
        GET_CTIME                   = 0x1E  # Запрос сетевого времени
        ECO_MODE_ON                 = 0x14  # Переключение сети в экономичный режим
        ECO_MODE_OFF                = 0x15  # Переключение сети в активный режим
        GET_TEMP_POWER              = 0x20  # Запрос температуры и напряжения питания
        GET_DEVICE_VERSION_REMOTE   = 0x23  # Запрос версии удалённого устройства
        ASK_NET_PARAMS              = 0x24  #  Запрос Id сети и основных параметров
        GET_NET_INFO                = 0x0E  # Запрос статусов устройств сети (в режиме совместимости)
        SET_RESEND_ADDR             = 0x0D  # Установка адреса пересылки
        SET_FCFG_RESEND_ADDR        = 0x1B  # Установка поля Resend структуры FCfg для заданного узла.

    class CmdSys(IntEnum):
        """Список подкоманд группы ModemCmdSys"""
        SHOW_LINX               = 0x05  # Запрос данных слышимости для заданного узла
        LINX                    = 0x11  # Данные о слышимости для определённого узла
        MY_STATUS               = 0x12  # Состояние своего модема.
        ROUTE_TABLE             = 0x15  # Маршрутная таблица
        ROUT_2                  = 0x1B  # Маршрутная таблица в режиме совместимости
        NET_INFO                = 0x1A  # Информация о статусе сесоров (в режиме совместимости)
        ASK_XTYP                = 0x17  # Запрос радиомодемом типа ВУ
        REMOTE_MODEM_STATUS     = 0x19  # Состояние удадённого модема
        MODEM_VERSION_REMOTE    = 0x1F  # Версия удалённого модема
        TEMP_POWER              = 0x20  # Температура и напряжение питания
        CTIME                   = 0x25  # Сетевое время
        DEVICE_VERSION_REMOTE   = 0x26  # Версия удалённого устройства
        NET_PARAMS              = 0x27  # Id сети и основные параметры

    class SendMode(IntEnum):
        Default = 0
        Urgent  = 0x20
        OneShot = 0x40
        Forced  = 0x80

    class ExtDevType(IntEnum):
        # Радиомодем без внешнего устройства. Используется в качестве автономного ретранслятора (АВР).
        NONE                = 0x00
        # Универсальный радиосигнализатор (РС-У), котором задействован сейсмический датчик. Обозначается как радиосигнализатор вибрационный (РС-В).
        SEISMIC             = 0x01
        # Универсальный радиосигнализатор (РС-У), котором задействован обрывной датчик. Обозначается как радиосигнализатор обрывного типа (РС-О).
        Wire                = 0x02
        # Универсальный радиосигнализатор (РС-У), котором задействован сейсмический и обрывной датчик.Обозначается как радиосигнализатор сейсмического и обрывного типа (РС-ВО).
        SEISMIC_WIRE        = 0x03
        # Универсальный радиосигнализатор (РС-У), котором задействован блок управления внешним устройством (БУВ). Обозначается как радиосигнализатор типа БУВ.
        BUV                 = 0x04
        # Универсальный радиосигнализатор (РСУ), котором задействован блок управления внешним устройством (БУВ) и сейсмический датчик. Обозначается как радиосигнализатор БУВ + РСВ (БУВ-В).
        BUV_SEISMIC         = 0x05
        # Универсальный радиосигнализатор (РСУ), котором задействован блок управления внешним устройством (БУВ) и датчик обрывного типа. Обозначается как радиосигнализатор БУВ + РСО (БУВ-О).
        BUV_WIRE            = 0x06
        # Универсальный радиосигнализатор (РСУ), котором задействован блок управления внешним устройством (БУВ), датчик и датчик обрывного типа.
        # Обозначается как радиосигнализатор БУВ + РСО + РСВ (БУВ-ВО).
        BUV_SEISMIC_WIRE    = 0x07
        # Переносимый контрольный приемник (КОПР).
        KOPR                = 0X08
        # Радиосигнализатор магнитного типа (РС-М).
        MAGNETIC            = 0x09
        # Радиосигнализатор инфракрасного типа (РС-ИК).
        IR                  = 0x0A
        # Видеокамера (РС-ТВ).
        PHOTO               = 0x0B
        # Универсальный радиосигнализатор (РС-У), котором не задействован ни один датчик. Обозначается как автономный ретранслятор (АВР).
        # Отличается от SENSOR_NONE наличием ВУ типа РС-У. Т.е., сейсмическую часть, SENSOR_RETR можно сделать SENSOR_SEISM и т.п.
        REPEATER            = 0x0C
        # Телевизионный ретранслятор (ТВ-Р).
        TVR                 = 0x0D
        # РС-ФР (Фоторегистратор)
        RS_FR               = 0x27
    
    class NetStatus:
        def __init__(self):
            # Узел синхронизирован с сетью
            self.connected = False
            # Ведущий
            self.master = False
            # Включена ретрансляция пакетов
            self.repeater = False
            # Есть таблица маршрутов
            self.have_route_table = False
            # Была выполнена первая рассылка данных о радиослышимости
            self.registered = False
            # Экономичный режим работы
            self.eco_mode = False
            # Нет ответа от внешнего устройства
            self.ext_dev_lost = False
            # Узел является шлюзом в сеть верхнего уровня
            self.gate = False

        def unpack(self, value: int):
            self.connected = value & 0x80
            self.master = value & 0x40
            self.repeater = value & 0x20
            self.have_route_table = value & 0x10
            self.registered = value & 0x08
            self.eco_mode = value & 0x04
            self.ext_dev_lost = value & 0x02
            self.gate = value & 0x01
        
    class Mode:
        def __init__(self):
            # Включен отладочный лог
            self.debug_log_enabled = False
            # Включено оповещение ВУ об изменениях статуса и слышимости
            self.show_news = False
            # Отображать в логе сбойные пакеты (bad checksum)
            self.show_bad_packets = False
            # Запрет экономичного режима приема
            self.eco_mode_disable = False
            # Пересылка на ВУ всех принятых пакетов
            self.overhear = False
            # Отключение линейного автомата статистики слышимости
            self.rf_protect = False
            # Обрыв антенны
            self.antenna_break = False
            # Включен или выключен режим пеленгации
            self.peleng_enabled = False

        def unpack(self, value: int):
            self.debug_log_enabled = value & 0x01
            self.show_news = value & 0x02
            self.show_bad_packets = value & 0x04
            self.eco_mode_disable = value & 0x08
            self.rf_protect = value & 0x10
            self.overhear = value & 0x20
            self.antenna_break = value & 0x40
            self.peleng_enabled = value & 0x80

    class LinkInfo:
        def __init__(self):
            # Логический номер узла в сети
            self.net_address = 0
            # Сетевой статус узла
            self.net_status = Modem.NetStatus()
            # Тип внешнего устройства узла
            self.ext_dev_type = Modem.ExtDevType.NONE
            # Внешнее устройство включено
            self.ext_dev_enabled = False
            # Статистика слышимости
            self.link_table = [int]
            # Состояние ВУ
            self.xstatus = 0
            self.valid = False
            
        def unpack(self, net_size: int, data: bytearray):
            valid_size = 3 + round(net_size / 4.0)
            self.valid = (0 < net_size <= 40) and (len(data) >= valid_size)
            if self.valid:
                self.net_address = data[0]
                self.net_status.unpack(data[1])
                self.ext_dev_type = Modem.ExtDevType(data[2] & 0x3F)
                self.ext_dev_enabled =  not (data[2] & 0x40)
                self.link_table.clear()
                for i in range(net_size):
                    self.link_table.append((data[3 + i // 4] >> ((i & 0x03) * 2)) & 0x03)
                if len(data) >= valid_size + 2:
                    self.xstatus = (data[valid_size + 0] + (data[valid_size + 1] << 8)) & 0xFFFF
            return self.valid



    class Info():
        def __init__(self):
            # Размерность сети
            self.ntwork_size = 0
            # Логический номер узла в сети
            self.net_address = 0
            # Сетевой статус узла
            self.net_status = Modem.NetStatus()
            # Тип внешнего устройства узла
            self.ext_dev_type = Modem.ExtDevType.NONE
            # Внешнее устройство включено
            self.ext_dev_enabled = False
            # Адрес пересылки (только для "нулевого")
            self.resend_address = 0xFF
            # Режим работы модема
            self.mode = Modem.Mode()
            # Номер частотного канала iF: 433000 + 200 * iF (кГц)
            self.frequency_channel = 0
            # Уровень выходной мощности модема: 0..3 – для модемов без усилителя, 0..7 для модемов с усилителем
            self.rf_power = 0
            # Число пакетов в буфере
            self.buffer_packet_count = 0
            # Серийный номер модема
            self.serial_number = 0
            # Температура по Цельсию
            self.temperature = 0
            # Напряжение на аккумуляторе в Вольтах * 100
            self.power_voltage = 0.0
            # Число перезапусков от WatchDog
            self.watchdog_reset_count = 0
            # Полное время с момента включения, или аппаратного перезапуска, в Секундах
            self.uptime = 0
            # старшая часть серийного номера
            self.serial_hi = 0
            self.valid = False

        def unpack(self, data: bytearray):
            self.valid = len(data) >= 20 - 1
            if self.valid:
                self.ntwork_size = data[0]
                self.net_address = data[1]
                self.net_status.unpack(data[2])
                self.ext_dev_type = Modem.ExtDevType(data[3] & 0x3F)
                self.ext_dev_enabled = not (data[3] & 0x40)
                self.resend_address = data[4]
                self.mode.unpack(data[5])
                self.frequency_channel = (data[6] >> 4) & 0x0F
                self.rf_power = data[6] & 0x0F
                self.buffer_packet_count = data[7]
                self.serial_number = data[8] + (data[9] << 8)
                self.temperature = data[10]
                self.power_voltage = (data[11] + (data[12] << 8)) / 100.0
                self.watchdog_reset_count = data[13] + (data[14] << 8)
                self.uptime = (data[15] + (data[16] << 8) + (data[17] << 16) + (data[18] << 24)) * 2
                self.serial_hi = data[19] if len(data) >= 20 else 0
            return self.valid

    def process_packet(self, packet: Packet):
        data = packet.data
        if self.Command(packet.command):
            if self.Command.PING:
                pass
            elif self.Command.SYS:
                if len(data) < 1:
                    return
                cmd_sys = data[0]
                data = data[1:]
                if self.CmdSys(cmd_sys):
                    if self.CmdSys.LINX:
                        info = self.info.get(self.self_net_address, self.Info)
                        linx = self.LinkInfo()
                        linx.unpack(info.ntwork_size, data)
                        if linx.valid:
                            self.link_info.update({linx.net_address: linx})
                    elif self.CmdSys.MY_STATUS:
                        info = self.Info()
                        info.unpack(data)
                        if info.valid:
                            self.info.update({info.net_address: info})
                            self.self_net_address = info.net_address
                    elif self.CmdSys.REMOTE_MODEM_STATUS:
                        info = self.Info()
                        info.unpack(data)
                        self.info.update({info.net_address: info})
                    elif self.CmdSys.ROUTE_TABLE:
                        if len(data) > 1:
                            table_size = data[0]
                            if len(data) >= 1 + table_size:
                                self.route_table = data[1:table_size+1]
                    else:
                        pass
            elif self.Command.DATA:
                pass
            else:
                pass

    def send_cmd(self, cmd: int, data = bytearray()):
        pkt = Packet()
        pkt.address_src = Packet.Address.PC
        pkt.address_dst = Packet.Address.MODEM
        pkt.command = cmd & 0xFF
        pkt.data = data
        if self.send_packet_callback:
            self.send_packet_callback(pkt)

    def send_cmd_ping(self):
        self.send_cmd(self.Command.PING)

    def send_cmd_show_status(self):
        self.send_cmd(self.Command.DO, bytearray([self.CmdDo.SHOW_STATUS]))
    
    def send_cmd_show_linx(self, addr: int):
        self.send_cmd(self.Command.DO, bytearray([self.CmdDo.SHOW_LINX, addr]))