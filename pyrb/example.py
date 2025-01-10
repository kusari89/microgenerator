from serial import Serial
from serial.threaded import ReaderThread, Protocol
import time
from rb.rb_device import RbDevice
from rb.serial_port import SerialPort


if __name__ == '__main__':
    ### Example-1
    print("########## Example-1: Main usage ##########")

    rb = RbDevice()

    def on_packet_received(packet):
        print("Packet received [" + str(rb.rx_packet_counter) + "]: " + str(rb.packet_to_dict(packet)) + "\n")

    rb.on_packet_received_callback = on_packet_received

    class SerialReader(Protocol):
        def connection_made(self, transport):
            print("Connected, ready to receive data...")

        def data_received(self, data):
            rb.process_raw_data(data)
        
        def connection_lost(self, exc):
            print("Connection lost... Error: " + str(exc))
    
    serial_port = Serial("/dev/ttyUSB3", 4800)
    serial_worker = ReaderThread(serial_port, SerialReader)
    serial_worker.start()

    rb.send_raw_data_callback = serial_port.write
    rb.send_cmd(rb.Address.MODEM, 0)  # Send PING command (cmd=0) to Modem
    rb.modem.send_cmd_ping()          # Same...
    rb.send_cmd_ping_sensor()         # Send PING command to Sensor
    rb.send_cmd(rb.Address.MODEM, 0x12, bytearray([0x02]))  # Send DO (0x12) command with subcommand SHOW_STATUS (0x02) to Modem
    rb.send_cmd(rb.Address.MODEM, rb.modem.Command.DO, bytearray([rb.modem.CmdDo.SHOW_ROUTE]))  # Send DO (0x12) command with subcommand SHOW_ROUTE (0x07) to Modem
    
    time.sleep(2)

    self_addr = rb.modem.self_net_address
    rb.modem.send_cmd_show_linx(0)  # Send cmd: ask link table from device at adress 0
    
    time.sleep(2)

    if self_addr >= 0:
        link_info_0 = rb.modem.link_info.get(0)
        print("Serial number:\t" + str(rb.modem.info.get(self_addr).serial_hi).zfill(5) + "-" + str(rb.modem.info[self_addr].serial_number).zfill(3))
        print("Net address:  \t" + str(rb.modem.info.get(self_addr).net_address))
        print("Device type:  \t" + str(rb.modem.info.get(self_addr).ext_dev_type.name))
        print("Net size:     \t" + str(rb.modem.info.get(self_addr).ntwork_size))
        print("Power voltage:\t" + str(rb.modem.info.get(self_addr).power_voltage) + "V")
        print("Temperature:  \t" + str(rb.modem.info.get(self_addr).temperature) + "°C")
        print("Route table:  \t" + str(list(rb.modem.route_table)))
        print("Link table:   \t" + (str(link_info_0.link_table) if link_info_0 else "???") + "\n")

    print("Tx packet count: " + str(rb.tx_packet_counter))
    print("Rx packet count: " + str(rb.rx_packet_counter))
    print("Rx bad checksum packet count: " + str(rb.rx_bad_packet_counter) + "\n")

    serial_worker.close()
    time.sleep(2)


    ### Example-2
    print("########## Example-2: Serial port baudrate autodetect ##########")

    ser_port = SerialPort()
    
    rb = ser_port.try_open("/dev/ttyUSB3")
    if rb:
        print("Device found: port: " + str(ser_port.port_name) + ", baudrate: " + str(ser_port.port_baudrate))
        rb.modem.send_cmd_show_status()
        time.sleep(2)
        print("Device type:  \t" + str(rb.modem.info.get(self_addr).ext_dev_type.name))
    else:
        print("Device not found")

    ser_port.close()
