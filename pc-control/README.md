# Bowmont Railway PC Control

Uses pygame for animation. Communicates with Arduino using PySerial

Top-level: [main.py](pc_control/main.py).

Settings can be found in [settings.toml](pyproject.toml).


## Install

Dependencies are managed with poetry. cd to the directory then:

```shell
poetry install
```

I reccomend [pipx](https://pypa.github.io/pipx/) to install [poetry](https://python-poetry.org/) and setting the venv directory to the project directory:

```shell
pip install pipx
pipx ensurepath
pipx install poetry
poetry config virtualenvs.in-project
```
