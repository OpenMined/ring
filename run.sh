#!/bin/sh
uv venv --allow-existing
# this will use syftbox coming from the app runner by default
# if that fails it will locate syftbox using the global uv tool path
# which ensures you get editable mode and stand-alone running in one line
uv run python -c 'import syftbox' 2>/dev/null || export PYTHONPATH=$(uv tool run syftbox path):$PYTHONPATH
uv run python main.py
