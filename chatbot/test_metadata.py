from chatbot.embeddings import EmbeddingModel
from chatbot.chroma_store import ChromaStore

embedder = EmbeddingModel()
db = ChromaStore()

query = "summarize my resume"

embedding = embedder.create_embedding(query)

results = db.search(
    query_embedding=embedding,
    top_k=5,
    where={
        "document": "resume.pdf"
    }
)

print()

print("="*50)

for chunk in results:

    print(chunk["document"])
    print(chunk["page"])
    print(chunk["text"][:120])
    print("-"*50)