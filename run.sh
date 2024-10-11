#!/bin/sh
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    uv venv .venv
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi
# uv pip install http://20.168.10.234:8080/wheel/syftbox-0.1.0-py3-none-any.whl
uv run python main.py
