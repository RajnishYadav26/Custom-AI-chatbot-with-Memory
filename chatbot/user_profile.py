import json
import os



class UserProfile:

    def __init__(self):

        self.folder = "profiles"

        os.makedirs(self.folder, exist_ok=True)

        self.file = os.path.join(
            self.folder,
            "user_profile.json"
        )

    def load_profile(self):

        if os.path.exists(self.file):

            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)

        return {}

    def save_profile(self, profile):

        with open(self.file, "w", encoding="utf-8") as f:

            json.dump(
                profile,
                f,
                indent=4,
                ensure_ascii=False
            )