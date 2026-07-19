class ReciprocalRankFusion:

    def __init__(self, k=60):
        self.k = k

    def fuse(self, semantic_results, keyword_results):

        scores = {}

        # Semantic ranking
        for rank, chunk in enumerate(semantic_results):

            chunk_id = chunk["chunk_id"]

            score = 1 / (self.k + rank + 1)

            if chunk_id not in scores:

                scores[chunk_id] = {
                    "chunk": chunk,
                    "score": 0
                }

            scores[chunk_id]["score"] += score

        # Keyword ranking
        for rank, chunk in enumerate(keyword_results):

            chunk_id = chunk["chunk_id"]

            score = 1 / (self.k + rank + 1)

            if chunk_id not in scores:

                scores[chunk_id] = {
                    "chunk": chunk,
                    "score": 0
                }

            scores[chunk_id]["score"] += score

        fused = sorted(
            scores.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        return [
            item["chunk"]
            for item in fused
        ]