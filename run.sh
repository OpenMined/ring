#!/bin/bash

# Define cron-style schedule (e.g., "32 18 17,21,29 11 mon,wed")
# Refer to https://crontab.guru/#*_*_*_*_*
SCHEDULE="* * * * *"

# Function to check if the current time matches the schedule
function check_schedule() {
    # Split schedule into components
    IFS=' ' read -r S_MIN S_HOUR S_DOM S_MONTH S_DOW <<< "$SCHEDULE"
    
    # Get current time components
    CUR_MIN=$(date +'%M')
    CUR_HOUR=$(date +'%H')
    CUR_DOM=$(date +'%d')
    CUR_MONTH=$(date +'%m')
    CUR_DOW=$(date +'%a' | tr '[:upper:]' '[:lower:]')  # Convert to lowercase (e.g., "mon")

    # Helper function to match a component (e.g., "18" or "mon,wed")
    function match_component() {
        local component=$1
        local value=$2
        if [[ "$component" == "*" ]] || [[ "$component" == *",$value,"* ]] || [[ "$component" == "$value" ]]; then
            return 0
        else
            return 1
        fi
    }

    # Match each component of the schedule against the current time
    match_component ",$S_MIN," "$CUR_MIN" &&
    match_component ",$S_HOUR," "$CUR_HOUR" &&
    match_component ",$S_DOM," "$CUR_DOM" &&
    match_component ",$S_MONTH," "$CUR_MONTH" &&
    match_component ",$S_DOW," "$CUR_DOW"
}

# Only run if the schedule matches
if ! check_schedule; then
    echo "Not the scheduled time to run. Exiting."
    exit 0
fi

# this will create venv from python version defined in .python-version
uv venv

# install requirements for the project
uv pip install -r requirements.txt

# run app using python from venv
uv run main.py
