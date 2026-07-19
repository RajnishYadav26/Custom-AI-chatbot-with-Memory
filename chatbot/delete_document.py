from chatbot.chroma_store import ChromaStore

db = ChromaStore()

db.delete_document(
    "resume.pdf"
)