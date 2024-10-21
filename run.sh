#!/bin/sh

# this will create venv from python version defined in .python-version
uv venv

# Ensure pip is installed and up-to-date
uv run python -m ensurepip --upgrade

# Note: we need to point to the pip against the python version
# since uv is sensitive to current environment
# so running this app from syftbox uses syftbox's uv environment, 
# instead of the app environent

# install requirements for the project
uv run python -m pip install -r requirements.txt

# run app using python from venv
uv run main.py 2>&1 | tee app.log