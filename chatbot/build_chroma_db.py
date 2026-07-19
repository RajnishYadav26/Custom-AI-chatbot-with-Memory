from chatbot.pdf_loader import PDFLoader
from chatbot.chunker import TextChunker
from chatbot.embeddings import EmbeddingModel
from chatbot.chroma_store import ChromaStore

print("=" * 60)
print("Building Chroma Database")
print("=" * 60)

loader = PDFLoader()
chunker = TextChunker()
embedder = EmbeddingModel()
db = ChromaStore()

pdf_path = "chatbot/documents/resume.pdf"

pages = loader.load_pdf(pdf_path)

chunks = chunker.split_pages(
    pages,
    "resume.pdf"
)

vectors = []

for chunk in chunks:

    embedding = embedder.create_embedding(
        chunk["text"]
    )

    chunk["embedding"] = embedding

    vectors.append(chunk)

# Delete old version if it exists
db.delete_document("resume.pdf")

# Add new version
db.add_documents(vectors)

print()
print("=" * 60)
print("Database Built Successfully")
print(f"Inserted {len(vectors)} chunks")
print("=" * 60)