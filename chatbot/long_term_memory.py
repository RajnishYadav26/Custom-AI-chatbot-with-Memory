import json
import os


class LongTermMemory:

    def __init__(self):

        self.file = "data/long_term_memory.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:
                json.dump({}, f)

    def load(self):

        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, memory):

        with open(self.file, "w") as f:
            json.dump(memory, f, indent=4)