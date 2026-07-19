from pdf_loader import PDFLoader
from chunker import TextChunker
from embeddings import EmbeddingModel
from vector_store import VectorStore

loader = PDFLoader()

text = loader.load_pdf(
    "chatbot/documents/resume.pdf"
)

chunker = TextChunker()

chunks = chunker.split_text(text)

embedder = EmbeddingModel()

vectors = embedder.create_embeddings(chunks)

store = VectorStore()

store.create_index(vectors)

store.save()

new_store = VectorStore()

new_store.load()

print("\nDatabase Loaded Successfully!")

print(len(new_store.metadata))

print("=" * 60)

print("Vector Database Created!")

print("=" * 60)

print("Vectors Stored:")

print(len(store.metadata))