class MemoryManager:

    def __init__(self):
        self.history = []

    def add_user_message(self, message):
        self.history.append({
            "role": "user",
            "text": message
        })

    def add_ai_message(self, message):
        self.history.append({
            "role": "model",
            "text": message
        })

    def get_history(self):
        return self.history

    def save_history(self):
        return self.history

    def load_history(self, history):
        self.history = history

    # ----------------------------
    # NEW (Phase 8)
    # ----------------------------
    def prune_history(self, keep_last=10):
        """
        Keep only the most recent messages.
        """
        if len(self.history) > keep_last:
            self.history = self.history[-keep_last:]