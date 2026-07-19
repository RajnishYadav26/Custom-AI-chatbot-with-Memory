from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded!")

    def create_embedding(self, text):

        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def create_embeddings(self, chunks):

        embeddings = []

        for chunk in chunks:

            vector = self.create_embedding(
                chunk["text"]
            )

            embeddings.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "document": chunk["document"],
                    "page": chunk["page"],
                    "text": chunk["text"],
                    "length": chunk["length"],
                    "embedding": vector
                }
            )

        return embeddings