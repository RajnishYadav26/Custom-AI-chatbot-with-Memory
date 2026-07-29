from rank_bm25 import BM25Okapi


class KeywordSearch:

    def __init__(self):
        self.documents = []
        self.bm25 = None

    # -----------------------------------
    # Build BM25 Index
    # -----------------------------------

    def build(self, chunks):

        if not chunks:
            print("No documents found. BM25 index skipped.")
            self.documents = []
            self.bm25 = None
            return

        self.documents = chunks

        tokenized = [
            chunk["text"].lower().split()
            for chunk in chunks
        ]

        if len(tokenized) == 0:
            print("No tokenized documents. BM25 skipped.")
            self.bm25 = None
            return

        self.bm25 = BM25Okapi(tokenized)

        print(f"BM25 Index Built ({len(chunks)} documents)")

    # -----------------------------------
    # Keyword Search
    # -----------------------------------

    def search(
        self,
        query,
        top_k=3
    ):

        if self.bm25 is None:
            return []

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(scores, self.documents),
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        for score, chunk in ranked[:top_k]:

            item = chunk.copy()
            item["bm25_score"] = float(score)

            results.append(item)

        return results