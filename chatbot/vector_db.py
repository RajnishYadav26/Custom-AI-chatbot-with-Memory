from chatbot.pdf_loader import PDFLoader
from chatbot.chunker import TextChunker
from chatbot.embeddings import EmbeddingModel
from chatbot.chroma_store import ChromaStore

print("Loading components...")

loader = PDFLoader()
chunker = TextChunker()
embedder = EmbeddingModel()
db = ChromaStore()

pdf_path = "chatbot/documents/resume.pdf"

print("Loading PDF...")
pages = loader.load_pdf(pdf_path)

print(f"Loaded {len(pages)} pages")

chunks = chunker.split_pages(
    pages,
    "resume.pdf"
)

print(f"Created {len(chunks)} chunks")

vectors = []

for chunk in chunks:
    embedding = embedder.create_embedding(chunk["text"])
    chunk["embedding"] = embedding
    vectors.append(chunk)

print(f"Generated {len(vectors)} embeddings")

db.update_document(vectors)

print("Document updated successfully!")