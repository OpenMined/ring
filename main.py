import os
from pathlib import Path
import json
from syftbox.lib import ClientConfig


class RingRunner:
    def __init__(self):
        self.client_config = ClientConfig.load(
            os.path.expanduser("~/.syftbox/client_config.json")
        )
        self.my_email = self.client_config["email"]
        self.my_home = (
            Path(self.client_config["sync_folder"])
            / self.my_email
            / "app_pipelines"
            / "ring"
        )
        self.syft_perm_json = {
            "admin": [self.my_email],
            "read": [self.my_email, "GLOBAL"],
            "write": [self.my_email, "GLOBAL"],
            "filepath": str(self.my_home / "_.syftperm"),
            "terminal": False,
        }
        self.running_folder = self.my_home / "running"
        self.done_folder = self.my_home / "done"
        self.folders = [self.running_folder, self.done_folder]
        self.secret_file = Path(os.path.abspath(__file__)).parent / "secret.txt"

    def setup_folders(self):
        print("Setting up the necessary folders.")
        for folder in self.folders:
            os.makedirs(folder, exist_ok=True)
            with open(folder / "dummy", "w") as f:
                pass
        with open(self.my_home / "_.syftperm", "w") as f:
            json.dump(self.syft_perm_json, f)

    def check_datafile_exists(self):
        files = []
        print(f"Please put your data files in {self.running_folder}.")
        for file in os.listdir(self.running_folder):
            if file.endswith(".json"):
                print("There is a file here.")
                files.append(os.path.join(self.running_folder, file))
        print(f"Found {len(files)} files in {self.running_folder}.")
        return files

    def data_read_and_increment(self, file_name):
        with open(file_name) as f:
            data = json.load(f)

        ring_participants = data["ring"]
        datum = data["data"]
        to_send_idx = data["current_index"] + 1

        if to_send_idx >= len(ring_participants):
            print("END TRANSMISSION.")
            to_send_email = None
        else:
            to_send_email = ring_participants[to_send_idx]

        # Read the secret value from secret.txt
        with open(self.secret_file, 'r') as secret_file:
            secret_value = int(secret_file.read().strip())

        # Increment datum by the secret value instead of 1
        data["data"] = datum + secret_value
        data["current_index"] = to_send_idx
        os.remove(file_name)
        return data, to_send_email

    def data_writer(self, file_name, result):
        with open(file_name, "w") as f:
            json.dump(result, f)

    def send_to_new_person(self, to_send_email, datum):
        output_path = (
            Path(os.path.abspath(__file__)).parent.parent.parent
            / to_send_email
            / "app_pipelines"
            / "ring"
            / "running"
            / "data.json"
        )
        print(f"Writing to {output_path}.")
        self.data_writer(output_path, datum)

    def terminate_ring(self):
        my_ring_runner.data_writer(self.done_folder / "data.json", datum)


if __name__ == "__main__":
    # Start of script. Step 1. Setup any folders that may be necessary.
    my_ring_runner = RingRunner()
    my_ring_runner.setup_folders()
    # Step 2. Check if you have received a data file in your input folder.
    file_names = my_ring_runner.check_datafile_exists()
    # Step 3. If you have found a data file, proceed. Else, nothing.
    if len(file_names) > 0:
        print("Found a data file! Let's go to work.")
        # For this example, this will always be 1. But we can in theory do more complicated logic.
        for file_name in file_names:
            # Step 4. Read the data_file, increment the number and send it to the next person.
            datum, to_send_email = my_ring_runner.data_read_and_increment(file_name)
            # Step 5. If there is another person in the ring, send it to them. Else, terminate.
            if to_send_email:
                my_ring_runner.send_to_new_person(to_send_email, datum)
            else:
                my_ring_runner.terminate_ring()
    else:
        print("No data file found. As you were, soldier.")
