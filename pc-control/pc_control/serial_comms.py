import tomllib
import serial


def read_connection_settings():
    with open(r"pc-control\settings.toml", "rb") as f:
        settings = tomllib.load(f)["serial"]

    return settings['port'], settings['baud']


class ZeroWaitSerial(serial.Serial):
    """A class designed to read lines with a zero timeout read."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=0)
        self.buffer = ""

    def read_available_lines(self):
        if (self.in_waiting > 0):
            self.buffer += self.read(self.in_waiting).decode('ascii') 

            lines = self.buffer.split("\n")
            self.buffer = lines[-1]
            return lines[:-1]
        else:
            return []

class DummySerial():
    """Can be used when serial is not available"""

    def __init__(self, *args, **kwargs):
        pass

    def write(self, string):
        print(f"Write: {string}")
        
    def read_available_lines(self):
        return []

if __name__ == "__main__":

    port, baud = read_connection_settings()
    
    ser = ZeroWaitSerial(port, baud)

    while True:
        lines = ser.read_available_lines()

        for line in lines:
            print(line)