from serial import Serial
from serial.threaded import ReaderThread, Protocol
import time
from .rb_device import RbDevice

rb = RbDevice()

class SerialPort():
    def __init__(self):
        self.BAUD_RATES = [19200, 4800]
        self.serial_port = Serial()
        self.serial_worker = ReaderThread(self.serial_port, self.SerialReader)
        rb.send_raw_data_callback = self.serial_port.write
        self.current_baudrate = 0

    def try_open(self, port: str):
        self.serial_port.port = port

        for br in self.BAUD_RATES:
            self.close()
            self.serial_port.baudrate = br
            self.serial_port.open()
            self.serial_worker = ReaderThread(self.serial_port, self.SerialReader)
            self.serial_worker.start()

            tryCnt = 5
            while tryCnt > 0:
                tryCnt -= 1
                rb.modem.send_cmd_ping()
                rb.send_cmd_ping_sensor()
                time.sleep(1)
                
                if rb.ping_ok:
                    return rb

            self.serial_worker.close()

        return None
    
    def close(self):
        try:
            self.serial_worker.close()
        except:
            pass

        if self.serial_port.isOpen():
            self.serial_port.close()
    
    @property
    def port_name(self):
        return self.serial_port.port
    
    @property
    def port_baudrate(self):
        return self.serial_port.baudrate

    class SerialReader(Protocol):
        def connection_made(self, transport):
            pass

        def data_received(self, data):
            rb.process_raw_data(data)
        
        def connection_lost(self, exc):
            pass