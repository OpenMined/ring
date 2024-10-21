#!/bin/sh

# this will create venv from python version defined in .python-version
uv venv


uv run python -m ensurepip --upgrade

# install requirements for the project
uv pip install -r requirements.txt

# run app using python from venv
+uv run main.py 2>&1 | tee app.log
