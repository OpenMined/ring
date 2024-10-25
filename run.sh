#!/bin/sh

# this will create venv from python version defined in .python-version
uv venv

# install requirements for the project
uv pip install -e ../syft/sdk

. .venv/bin/activate

which python

# run app using python from venv
python main.py

deactivate
