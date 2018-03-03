
class ErrorModbus(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return "ErrorModbus : {}".format(self.message)

class ErrorModbusTcp0x01(Exception):

    def __init__(self):
        self.code = "0x01"
        self.message = "The used function code is not supported."

    def __str__(self):
        return "[ERROR - CODE - {}] : {}".format(self.code, self.message)

class ErrorModbusTcp0x02(Exception):

    def __init__(self):
        self.code = "0x02"
        self.message = "The register address used is not allowed. The register address may be invalid or write-protected."

    def __str__(self):
        return "[ERROR - CODE - {}] : {}".format(self.code, self.message)

class ErrorModbusTcp0x03(Exception):

    def __init__(self):
        self.code = "0x03"
        self.message = "Some data values used are out of range, i.e. invalid number of registers."

    def __str__(self):
        return "[ERROR - CODE - {}] : {}".format(self.code, self.message)

class ErrorModbusTcp0x06(Exception):

    def __init__(self):
        self.code = "0x06"
        self.message = "Device can not handle the request at the moment. Repeat the request."

    def __str__(self):
        return "[ERROR - CODE - {}] : {}".format(self.code, self.message)

class ErrorModbusTcp0x0B(Exception):

    def __init__(self):
        self.code = "0x0B"
        self.message = "Error message of the interconnected gateway: No response of the accessed device."

    def __str__(self):
        return "[ERROR - CODE - {}] : {}".format(self.code, self.message)
