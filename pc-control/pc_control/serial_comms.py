import tomllib
import serial
from time import sleep

def connect():
    with open("settings.toml", "rb") as f:
        settings = tomllib.load(f)["serial"]
    
    print(settings['port'])
    print(settings['baud'])

    ser = serial.Serial(settings['port'], settings['baud'], timeout=0.1)

    while True:

        data = ser.readlines()

        for line in data:
            try:
                print(line.decode('ascii'))
            except:
                print('decode fail')

        sleep(0.1)

if __name__ == "__main__":
    connect()