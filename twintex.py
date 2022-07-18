import binascii
from serial import Serial


class Twintex(Serial):
    def __init__(self, port, baudrate=9600, timeout=0.1, bytesize=8, parity='N', stopbits=1):
        super().__init__(port)
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        
    def send(self, command):
        str_val = command.encode('utf-8')
        hex_val = binascii.hexlify(str_val).decode('utf-8')+'0a'
        bytes_val = bytes.fromhex(hex_val)

        self.write(bytes_val)
        self.flush()
        return self.readline().decode('utf-8')

if __name__ == "__main__":
    Twintex = Twintex('COM4')

    # enter command according to the user manual
    print(Twintex.send(':APPL?'))
