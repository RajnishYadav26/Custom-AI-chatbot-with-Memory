from sentence_transformers import util
import numpy as np

from chatbot.embeddings import EmbeddingModel


class MemoryCompressor:

    def __init__(self, threshold=0.90):

        self.threshold = threshold

        self.embedder = EmbeddingModel()

    def compress(self, memories):

        if len(memories) <= 1:
            return memories

        compressed = []

        used = set()

        # Create embeddings for retrieved memories
        embeddings = []

        for memory in memories:

            vector = self.embedder.create_embedding(
                memory["text"]
            )

            embeddings.append(vector)

        for i in range(len(memories)):

            if i in used:
                continue

            current = memories[i]

            for j in range(i + 1, len(memories)):

                if j in used:
                    continue

                score = util.cos_sim(
                    np.array(embeddings[i]),
                    np.array(embeddings[j])
                ).item()

                if score >= self.threshold:

                    importance_i = current["metadata"].get(
                        "importance",
                        0
                    )

                    importance_j = memories[j]["metadata"].get(
                        "importance",
                        0
                    )

                    if importance_j > importance_i:

                        current = memories[j]

                    used.add(j)

            compressed.append(current)

        return compressed