from chatbot.embeddings import EmbeddingModel
from chatbot.chroma_store import ChromaStore

embedder = EmbeddingModel()

db = ChromaStore()

query = "Summarize my resume"

embedding = embedder.create_embedding(query)

results = db.search(
    embedding,
    top_k=3
)

for chunk in results:

    print("=" * 50)

    print(chunk["chunk_id"])

    print(chunk["document"])

    print(chunk["page"])

    print(chunk["distance"])

    print(chunk["text"][:200])