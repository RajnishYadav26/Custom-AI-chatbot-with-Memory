from sentence_transformers import CrossEncoder


class ReRanker:

    def __init__(self):

        print("Loading Cross Encoder...")

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print("Cross Encoder Loaded!")

    def rerank(
    self,
    query,
    chunks,
    top_k=3,
    threshold=6.0
):

        if not chunks:
            return []

        pairs = []

        for chunk in chunks:

            pairs.append(
                (
                    query,
                    chunk["text"]
                )
            )

        scores = self.model.predict(
            pairs
        )

        for chunk, score in zip(
            chunks,
            scores
        ):

            chunk["rerank_score"] = float(score)

        chunks.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        print("\n===== RERANK SCORES =====")

        filtered_chunks = []

        for chunk in chunks:

            print(
               chunk["chunk_id"],
               chunk["rerank_score"]
    )

            if chunk["rerank_score"] >= threshold:
                filtered_chunks.append(chunk)

        print("=========================\n")

        return filtered_chunks[:top_k]