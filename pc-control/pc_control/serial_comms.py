import tomllib

def connect():
    with open("settings.toml", "rb") as f:
        settings = tomllib.load(f)["serial"]
    
    print(settings['port'])
    print(settings['baud'])


if __name__ == "__main__":
    connect()