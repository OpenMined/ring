#!/bin/sh

set -e

# this will create venv from python version defined in .python-version
uv venv

# Activate the virtual environment using the dot command
. .venv/bin/activate

# install requirements for the project
uv pip install -r requirements.txt

# run app using python from venv
uv run main.py
