import tomllib
import serial


def read_connection_settings():
    with open("settings.toml", "rb") as f:
        settings = tomllib.load(f)["serial"]

    return settings['port'], settings['baud']


class ZeroWaitSerial():
    """A class designed to read lines with a zero timeout read."""

    def __init__(self, port, baud):

        self.ser = serial.Serial(port, baud, timeout=0)
        self.buffer = ""

    def read_available_lines(self):
        if (self.ser.in_waiting > 0):
            self.buffer += self.ser.read(self.ser.in_waiting).decode('ascii') 

            lines = self.buffer.split("\n")
            self.buffer = lines[-1]
            return lines[:-1]
        else:
            return []

if __name__ == "__main__":
    
    ser = ZeroWaitSerial(*read_connection_settings())

    while True:
        lines = ser.read_available_lines()

        for line in lines:
            print(line)