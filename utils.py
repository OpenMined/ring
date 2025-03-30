import json
from pathlib import Path
from syft_core.permissions import SyftPermission
import shutil

def write_json(file_path: Path, result: dict) -> None:
    print(f"Writing to {file_path}.")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(result, f)

def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def setup_folders(running_folder, done_folder, ring_pipeline_folder, data_template_file, client) -> None:
    print("Setting up the necessary folders.")

    if not running_folder.is_dir():
        for folder in [running_folder, done_folder]:
            folder.mkdir(parents=True, exist_ok=True)
            with open(folder / "dummy", "w") as dummy_file:
                dummy_file.write("\n")
        shutil.copy(data_template_file, ring_pipeline_folder / "data.json")

    permission = SyftPermission.mine_with_public_write(client, ring_pipeline_folder)
    permission.save(ring_pipeline_folder)
