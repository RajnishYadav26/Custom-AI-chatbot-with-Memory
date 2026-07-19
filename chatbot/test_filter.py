from chatbot.embeddings import EmbeddingModel
from chatbot.chroma_store import ChromaStore

embedder = EmbeddingModel()
db = ChromaStore()

query = "Summarize my resume"

embedding = embedder.create_embedding(query)

results = db.search(
    query_embedding=embedding,
    top_k=5,
    where={
        "document": "resume.pdf"
    }
)

print("=" * 60)

for chunk in results:

    print(chunk["document"])

    print(chunk["page"])

    print(chunk["text"][:200])

    print("-" * 60)