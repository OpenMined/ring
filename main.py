import os
from pathlib import Path
import shutil
from typing import List
from syftbox_sdk import SyftBoxContext
from pydantic import BaseModel
from pydantic_core import from_json

RING_APP_PATH = Path(os.path.abspath(__file__)).parent
INIT_DATA = Path(RING_APP_PATH / "data.json")


class RingData(BaseModel):
    participants: list[str]
    data: int
    current_index: int

    @property
    def ring_length(self) -> int:
        return len(self.participants)

    @classmethod
    def load_json(cls, file):
        with open(file, "r") as f:
            return cls(**from_json(f.read()))


class RingRunner:
    def __init__(self):
        self.client = SyftBoxContext.load()

        # this is where all the app state goes
        self.ring_data = self.client.get_app_data("ring")

        # this is where the pending inputs go
        self.running_folder: Path = self.ring_data / "running"

        # this is where the final result goes of a completed ring
        self.done_folder: Path = self.ring_data / "done"

        # this is your personal secret
        self.secret_file: Path = RING_APP_PATH / "secret.txt"

    def run(self) -> None:
        self.setup_folders()
        input_files = self.pending_inputs_files()
        for file_name in input_files:
            self.process_input(file_name)

        if len(input_files) == 0:
            print("No data file found. As you were, soldier.")

    def process_input(self, file_path) -> None:
        print(f"Found input {file_path}! Let's get to work.")

        ring_data = RingData.load_json(file_path)

        ring_data.data += self.my_secret()
        next_index = ring_data.current_index + 1

        if next_index < ring_data.ring_length:
            next_person = ring_data.participants[next_index]
            ring_data.current_index = next_index
            self.send_data(next_person, ring_data)
        else:
            self.terminate_ring(ring_data)

        self.cleanup(file_path)

    def cleanup(self, file_path: Path) -> None:
        file_path.unlink()
        print(f"Done processing {file_path}, removed from pending inputs")

    def setup_folders(self) -> None:
        print("Setting up the necessary folders.")
        self.client.make_dirs(self.running_folder, self.done_folder)
        self.client.set_writable(self.ring_data)

        shutil.copy(INIT_DATA, self.running_folder / "data.json")

    def my_secret(self) -> int:
        with open(self.secret_file, "r") as secret_file:
            return int(secret_file.read().strip())

    def pending_inputs_files(self) -> List[Path]:
        return [path.absolute() for path in self.running_folder.glob("*.json")]

    def write_json(self, file_path: Path, result: RingData) -> None:
        print(f"Writing to {file_path}.")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            f.write(result.model_dump_json(indent=2))

    def send_data(self, email: str, data: RingData) -> None:
        their_ring_data = self.client.get_app_data("ring", datasite=email)
        their_running = their_ring_data / "running"
        self.write_json(their_running / "data.json", data)

    def terminate_ring(self, data: RingData) -> None:
        print(f"Terminating ring, writing back to {self.done_folder}")
        self.write_json(self.done_folder / "data.json", data)


if __name__ == "__main__":
    runner = RingRunner()
    runner.run()
