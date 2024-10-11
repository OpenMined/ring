#!/bin/sh
uv venv --allow-existing
uv pip install --upgrade syftbox
uv run python main.py
