from embeddings import EmbeddingModel
from vector_store import VectorStore

embedder = EmbeddingModel()

store = VectorStore()

store.load()

question = "What is Machine Learning?"

query_embedding = embedder.create_embedding(
    question
)

results = store.search(
    query_embedding,
    top_k=3
)

for i, result in enumerate(results):

    print("=" * 60)

    print("Result", i + 1)

    print("-" * 60)

    print(result["text"])