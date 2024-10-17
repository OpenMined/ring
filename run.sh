#!/bin/sh

# this will create venv from python version defined in .python-version
uv venv

# install requirements for the project
uv pip install -r requirements.txt

# run app using python from venv
uv run main.py
