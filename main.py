import os
import sys
from pathlib import Path
from syft_core import Client
from utils import load_json, write_json, setup_folders
from typing import List

def load_ring_data(file_path: Path):
    ring_data = load_json(file_path)
    return ring_data["participants"], ring_data["data"], ring_data["current_index"]

def create_ring_data(participants: List[str], data: int, current_index: int):
    return {"participants": participants, "data": data, "current_index": current_index}

client = Client.load()
my_email: str = client.email

RING_APP_PATH = Path(os.path.abspath(__file__)).parent
RING_PIPELINE_FOLDER = client.app_data("ring")
RUNNING_FOLDER = RING_PIPELINE_FOLDER / "running"
DONE_FOLDER = RING_PIPELINE_FOLDER / "done"
SECRET_FILE = RING_APP_PATH / "secret.json"
DATA_TEMPLATE_FILE = RING_APP_PATH / "data.json"

my_secret = load_json(SECRET_FILE)["data"]
setup_folders(RUNNING_FOLDER, DONE_FOLDER, RING_PIPELINE_FOLDER, DATA_TEMPLATE_FILE, client)
pending_inputs_files = [RUNNING_FOLDER / file for file in RUNNING_FOLDER.glob("*.json")]

if len(pending_inputs_files) == 0:
    print("No data file found. As you were, soldier.")
    sys.exit(0)

file_path = pending_inputs_files[0]
print(f"Found input {file_path}! Let's get to work.")

try:
    ring_participants, data, current_index = load_ring_data(file_path)
except Exception:
    print("It seems something is not set. Skipping it for now")
    exit()
data += my_secret
next_index = current_index + 1

if next_index < len(ring_participants):
    next_person = ring_participants[next_index]
    new_ring_data = create_ring_data(ring_participants, data, next_index)
    receiver_ring_data = client.app_data("ring", datasite=next_person) / "running" / "data.json"
    write_json(receiver_ring_data, new_ring_data)
else:
    print(f"Terminating ring, writing back to {DONE_FOLDER}")
    final_ring_data = create_ring_data(ring_participants, data, current_index)
    write_json(DONE_FOLDER / "data.json", final_ring_data)

file_path.unlink()
print(f"Done processing {file_path}, removed from pending inputs")

