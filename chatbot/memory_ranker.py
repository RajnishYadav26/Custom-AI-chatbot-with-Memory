from datetime import datetime


class MemoryRanker:

    def __init__(self):

        # Weight of each signal
        self.semantic_weight = 0.50
        self.importance_weight = 0.20
        self.recency_weight = 0.15
        self.frequency_weight = 0.15

    def rank(self, memories):

        ranked = []

        for memory in memories:

            semantic = memory.get("score", 0)

            importance = memory.get("importance", 0.5)

            frequency = memory.get("usage_count", 1)

            timestamp = memory.get("timestamp", "")

            recency = self.calculate_recency(timestamp)

            final_score = (
                semantic * self.semantic_weight
                + importance * self.importance_weight
                + recency * self.recency_weight
                + frequency * self.frequency_weight
            )

            memory["final_score"] = final_score

            ranked.append(memory)

        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return ranked

    def calculate_recency(self, timestamp):

        if not timestamp:
            return 0

        try:

            t = datetime.fromisoformat(timestamp)

            days = (datetime.now() - t).days

            return 1 / (1 + days)

        except Exception:

            return 0