from chatbot.chroma_store import ChromaStore

db = ChromaStore()

print(db.collection.count())