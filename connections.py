
import sys
import socket
import threading

from mdlmodbus.specifics.templates import ModbusTCPFrame, ModbusRTUFrame, ModbusThreadRead, ModbusThreadWrite
from bases import BaseBinder, BaseCommand
from mdlutils.network import ipv4

# Ayncronous modbus : TCP/IP (Modbus Ethernet) 
class ModbusTcpBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)
        self.host = ipv4()
        self.port = 502

    def initialize(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.observable.parent.observable.status = True
            print("[SUCCESS - BINDER - MODBUS] : Connection (host: {}, port: {})".format(self.host, self.port))
        except Exception as e:
            print("ErrorModbus : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 
            self.socket.close()

    def run(self):
        self.thMdbR = ModbusThreadRead(self.socket, self.read)
        self.thMdbR.start()
        self.thMdbR.join()


    def execute(self, data):
        if self.socket._closed != True:
            if data == BaseCommand.RUN:
                self.run()
            else:
                self.write()

    def read(self, data):
        pass
        
    def write(self):
        data = [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0x05, 0x07, 0x9A]
        self.thMdbW = ModbusThreadWrite(self.socket, data)
        self.thMdbW.start()
        self.thMdbW.join()
        print("write")

# Syncronous modbus : RS-485
class ModbusRtuBinder(BaseBinder):
    
    def __init__(self, name, observable=None):
        super().__init__(name, observable)

    def initialize(self):
        pass

    def read(self):
        data = "Modbus RTU Binder"
        # crc = ModbusTcpBinder.crc16(frame)
        # print(crc)
        # frame.append(str(ModbusTcpBinder.high_byte(crc)))
        # frame.append(str(ModbusTcpBinder.low_byte(crc)))
        self.observable.emit(data)

    def write(self):
        pass
    
