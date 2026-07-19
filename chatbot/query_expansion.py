class QueryExpansion:

    def __init__(self):

        self.dictionary = {

            "ai": [
                "artificial intelligence",
                "machine learning",
                "deep learning",
                "neural network"
            ],

            "ml": [
                "machine learning",
                "artificial intelligence",
                "supervised learning"
            ],

            "python": [
                "programming",
                "coding",
                "language"
            ],

            "database": [
                "sql",
                "nosql",
                "storage"
            ],

            "rag": [
                "retrieval",
                "vector database",
                "embedding"
            ],

            "llm": [
                "large language model",
                "transformer",
                "generative ai"
            ]
        }

    def expand(self, query):

        expanded = query.lower()

        words = query.lower().split()

        for word in words:

            if word in self.dictionary:

                expanded += " "

                expanded += " ".join(
                    self.dictionary[word]
                )

        return expanded