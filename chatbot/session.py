import json
import os
from datetime import datetime


class SessionManager:

    def __init__(self):
        # Folder where all chat sessions are stored
        self.session_folder = "sessions"

        # Create the folder if it doesn't exist
        os.makedirs(self.session_folder, exist_ok=True)

        # Generate a unique session ID
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create the JSON file path
        self.file_path = os.path.join(
            self.session_folder,
            f"{self.session_id}.json"
        )

    def save_session(self, history):
        """Save chat history to a JSON file."""

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False
            )

    def load_session(self):
        """Load chat history from the current session file."""

        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def list_sessions(self):
        """Display all saved session files."""

        files = os.listdir(self.session_folder)

        print("\n===== Saved Sessions =====\n")

        if not files:
            print("No saved sessions found.")
            return

        for file in files:
            print(file)