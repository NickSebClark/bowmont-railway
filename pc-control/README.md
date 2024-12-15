# Bowmont Railway PC Control

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Uses pygame for animation. Communicates with Arduino using PySerial

Top-level: [main.py](pc_control/main.py).

Settings can be found in [settings.toml](settings.toml).


## Install

Dependencies are managed with [uv](https://docs.astral.sh/uv/). cd to the directory and get started with:

```shell
uv run main
```

The project is configured as a package. This tells uv to install pc_control as an editable package in the environment. This way, imports can always be relative to this package.

main.py is added as a script so we can access it easily with uv run.