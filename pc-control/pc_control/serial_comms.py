import tomllib
import serial

def read_connection_settings():
    with open("settings.toml", "rb") as f:
        settings = tomllib.load(f)["serial"]

    return settings['port'], settings['baud']

def connect():

    port, baud = read_connection_settings()

    return serial.Serial(port, baud, timeout=0)

def read_data(ser:serial.Serial):

    lines = ser.readlines()

    return [line.decode('ascii') for line in lines]

if __name__ == "__main__":
    connect()