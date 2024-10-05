#!/bin/sh
uv venv .venv
uv pip install http://20.168.10.234:8080/wheel/syftbox-0.1.0-py3-none-any.whl
uv run python main.py