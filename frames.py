
""" 
    MODBUS protocol
    
    Modbus RTU (Remote Terminal Unit)
    Only one master.
    [START|B0|B1|B2|B3|B4|B5|B6|B7|STOP|STOP]
    [START|B0|B1|B2|B3|B4|B5|B6|B7|PARITE|STOP]
    PARITE : Pair (even) or Impair (odd)

    Modbus TCP allow the multi-masters

    CRC (Cyclical Redundancy Check) - test de refondance cyclique
    The crc is on 16 bits / 0x0000

    Proctocol PHY modbus:
        * RS-232
        * RS-485
        * RS-422
        * TCP/IP (Modbus Ethernet)

    MODBUS FRAME RTU :
        * Start : silence
        * Slave adress : 0x00
        * Code function : 0x00
        * Data : 0xn...
        * CRC : 0x0000
        * End : silence
"""

import sys
import threading

from mdlutils.utils import *
from mdlmodbus.specifics.exceptions import *

""" CRC 16 CALCULATION """
INITIAL_MODBUS = 0xFFFF
INITIAL_POLY = 0xA001

""" TCP/IP ERRORS """ 
ERROR_CODES = {"0x01": ErrorModbusTcp0x01, "0x02": ErrorModbusTcp0x02 , "0x03": ErrorModbusTcp0x03, "0x06": ErrorModbusTcp0x06, "0x0B": ErrorModbusTcp0x0B}

class MBAPHeader:

    def __init__(self, num_trans=0, proto=0, lendata1=0, lendata2=0):
        self.num_trans = num_trans
        self.proto = proto
        self.lendata1 = lendata1
        self.lendata2 = lendata2

class ModbusTCPFrame:

    def __init__(self, data):
        self.header = MBAPHeader()
        self.payload = data

    def serialize(self):
        print(self.payload)
        function = int(self.payload[1]) & 0xFF
        if function == 0x06:
            devaddr = int(self.payload[3]) & 0xFF
            regaddr = int(self.payload[5]) & 0xFFFF
            value = int(self.payload[7]) & 0xFFFF 
            frame = [
                chr(0 & 0xFF),
                chr(self.header.num_trans & 0xFF),
                chr(0 & 0xFF),
                chr(self.header.proto & 0xFF),
                chr(self.header.lendata1 & 0xFF),
                chr(self.header.lendata2 & 0xFF),
                chr(devaddr & 0xFF),
                chr(function & 0xFF),
                chr(0 & 0xFF),
                chr(regaddr & 0xFF),
                chr(0 & 0xFF),
                chr(value & 0xFF)]
            print(frame)
            # data = [0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0x05, 0x07, 0x9A]
            return list2str([chr(d) for d in frame])

    def deserialize(self):
        pass

class ModbusRTUFrame:

    def __init__(self):
        pass

    def __crc16(self, frame=[]):
        crc = INITIAL_MODBUS 
        poly = INITIAL_POLY
        for b in frame:
            crc ^= bytes2int(b)
            for i in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= poly
                else:
                    crc = crc >> 1 
        swap = ((crc << 8) & 0xff00) | ((crc >> 8) & 0x00ff)
        return swap

class ModbusThreadRead(threading.Thread):

    PACKET_SIZE = 1024

    def __init__(self, connection, callback):
        super().__init__()
        self.connection = connection
        self.callback = callback
        self.name = self.getName()
        self.isRunning = False
        self.treat = ModbusTreatResponse()

    def run(self):
        self.isRunning = True
        while self.isRunning:
            try:
                msg = self.connection.recv(ModbusThreadRead.PACKET_SIZE)
                self.treat._decode_mdbs_response(msg)
                self.callback(msg)
            except Exception as e:
                print("ErrorRead : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e))
                self.stop()

    def stop(self):
        self.isRunning = False

class ModbusThreadWrite(threading.Thread):

    def __init__(self, connection, data):
        super().__init__()
        self.connection = connection
        self.data = str(list2str([chr(d) for d in data]))
        self.name = self.getName()

    def run(self):
        try: 
            self.connection.send(self.data.encode())
        except Exception as e:
            print("ErrorWrite : ligne {} - {}".format(sys.exc_info()[-1].tb_lineno, e)) 

class ModbusTreatResponse:

    def __init__(self):
        pass

    def _decode_mdbs_response(self, resp):
        for code in ERROR_CODES:
            if resp[len(resp)-1] == int(code, 16):
                raise ERROR_CODES[code]()
        for c in resp:
            print("|{}".format(c ^ 0x00), end='|')
        print()

class ModbusTreatRequest:

    @staticmethod
    def treat(data):
        print(data)
        data["func"] = chr(hex(data["func"]))
        data["dev"] = chr(hex(data["func"]))
        data["reg"] = chr(hex(data["func"]))
        data["val"] = chr(hex(data["func"]))
