class RetrievalMetrics:

    def precision_at_k(self, retrieved, relevant):

        if len(retrieved) == 0:
            return 0

        correct = 0

        for chunk in retrieved:

            if chunk["chunk_id"] in relevant:
                correct += 1

        return correct / len(retrieved)

    def recall_at_k(self, retrieved, relevant):

        if len(relevant) == 0:
            return 0

        correct = 0

        for chunk in retrieved:

            if chunk["chunk_id"] in relevant:
                correct += 1

        return correct / len(relevant)

    def hit_rate(self, retrieved, relevant):

        for chunk in retrieved:

            if chunk["chunk_id"] in relevant:
                return 1

        return 0

    def mrr(self, retrieved, relevant):

        for i, chunk in enumerate(retrieved):

            if chunk["chunk_id"] in relevant:
                return 1 / (i + 1)

        return 0